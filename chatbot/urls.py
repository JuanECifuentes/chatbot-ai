from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chatbot.views import ConversationViewSet, ChatViewSet, chat_interface

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'chat', ChatViewSet, basename='chat')

urlpatterns = [
    path('', include(router.urls)),
]
