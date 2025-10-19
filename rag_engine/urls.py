from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rag_engine.views import SourceDocumentViewSet, DocumentChunkViewSet, RAGQueryLogViewSet

router = DefaultRouter()
router.register(r'documents', SourceDocumentViewSet, basename='document')
router.register(r'chunks', DocumentChunkViewSet, basename='chunk')
router.register(r'query-logs', RAGQueryLogViewSet, basename='query-log')

urlpatterns = [
    path('', include(router.urls)),
]
