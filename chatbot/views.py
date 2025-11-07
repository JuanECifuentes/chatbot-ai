from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from chatbot.models import Conversation, Message, User
from chatbot.serializers import (
    ConversationSerializer, ConversationListSerializer,
    MessageSerializer, ChatRequestSerializer, ChatResponseSerializer
)
from rag_engine.rag_service import RAGEngine
from rag_engine.models import RAGQueryLog


def chat_interface(request):
    """Render the chat interface"""
    return render(request, 'chatbot/chat_interface.html')


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing conversations"""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ConversationListSerializer
        return ConversationSerializer

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else User.objects.first()
        serializer.save(user=user)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get all messages for a conversation"""
        conversation = self.get_object()
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class ChatViewSet(viewsets.ViewSet):
    """ViewSet for chat interactions"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rag_engine = RAGEngine()

    @action(detail=False, methods=['post'])
    def send_message(self, request):
        """Send a message and get AI response"""
        serializer = ChatRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        message_content = data['message']
        conversation_id = data.get('conversation_id')
        instruction = data.get('instruction', '')
        top_k = data.get('top_k', 5)

        user = request.user if request.user.is_authenticated else User.objects.first()

        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id)
        else:
            conversation = Conversation.objects.create(
                user=user,
                title=message_content[:50]
            )

        user_message = Message.objects.create(
            conversation=conversation,
            sender='user',
            content=message_content
        )

        conversation_history = list(conversation.messages.values('sender', 'content'))

        query = f"{instruction}\n{message_content}" if instruction else message_content

        rag_result = self.rag_engine.generate_rag_response(
            query=query,
            conversation_history=conversation_history,
            top_k=top_k
        )

        assistant_message = Message.objects.create(
            conversation=conversation,
            sender='assistant',
            content=rag_result['response']
        )

        rag_log = RAGQueryLog.objects.create(
            conversation=conversation,
            query=query,
            response=rag_result['response'],
            execution_time=rag_result['execution_time']
        )
        rag_log.chunks_used.set(rag_result['chunks_used'])

        response_data = {
            'conversation_id': conversation.id,
            'message': MessageSerializer(user_message).data,
            'response': MessageSerializer(assistant_message).data,
            'chunks_used': rag_result['num_chunks'],
            'execution_time': rag_result['execution_time']
        }

        return Response(response_data, status=status.HTTP_200_OK)

