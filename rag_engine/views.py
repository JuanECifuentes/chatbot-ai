import os
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from rag_engine.models import SourceDocument, DocumentChunk, RAGQueryLog
from rag_engine.serializers import (
    SourceDocumentSerializer, DocumentChunkSerializer,
    RAGQueryLogSerializer, DocumentUploadSerializer
)
from document_processor.ingestion_service import DocumentIngestionService


class SourceDocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing source documents"""
    queryset = SourceDocument.objects.all()
    serializer_class = SourceDocumentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingestion_service = DocumentIngestionService()

    @action(detail=False, methods=['post'])
    def upload(self, request):
        """Upload and ingest a document"""
        serializer = DocumentUploadSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = serializer.validated_data['file']
        title = serializer.validated_data.get('title', '')
        author = serializer.validated_data.get('author', '')
        metadata = serializer.validated_data.get('metadata', {})

        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        if file_extension not in ['.pdf', '.docx']:
            return Response(
                {'error': 'Only PDF and DOCX files are supported'},
                status=status.HTTP_400_BAD_REQUEST
            )

        media_root = settings.MEDIA_ROOT
        os.makedirs(media_root, exist_ok=True)
        
        file_path = os.path.join(media_root, uploaded_file.name)
        
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        try:
            user = request.user if request.user.is_authenticated else None
            
            document = self.ingestion_service.ingest_document(
                file_path=file_path,
                title=title or uploaded_file.name,
                author=author,
                user=user,
                additional_metadata=metadata
            )

            serializer = SourceDocumentSerializer(document)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def reindex(self, request, pk=None):
        """Reindex a document"""
        try:
            document = self.ingestion_service.reindex_document(pk)
            serializer = SourceDocumentSerializer(document)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SourceDocument.DoesNotExist:
            return Response(
                {'error': 'Document not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'])
    def chunks(self, request, pk=None):
        """Get all chunks for a document"""
        document = self.get_object()
        chunks = document.chunks.all()
        serializer = DocumentChunkSerializer(chunks, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Delete a document"""
        document = self.get_object()
        success = self.ingestion_service.delete_document(document.id)
        
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Failed to delete document'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class DocumentChunkViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing document chunks"""
    queryset = DocumentChunk.objects.all()
    serializer_class = DocumentChunkSerializer


class RAGQueryLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing RAG query logs"""
    queryset = RAGQueryLog.objects.all()
    serializer_class = RAGQueryLogSerializer

