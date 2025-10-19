from django.contrib import admin
from rag_engine.models import SourceDocument, DocumentChunk, RAGQueryLog


@admin.register(SourceDocument)
class SourceDocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'file_type', 'file_size', 'upload_date', 'uploaded_by']
    list_filter = ['file_type', 'upload_date']
    search_fields = ['title', 'author']
    ordering = ['-upload_date']
    raw_id_fields = ['uploaded_by']


@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ['id', 'document', 'chunk_index', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'document__title']
    ordering = ['document', 'chunk_index']
    raw_id_fields = ['document']

    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'


@admin.register(RAGQueryLog)
class RAGQueryLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'query_preview', 'conversation', 'timestamp', 'execution_time']
    list_filter = ['timestamp']
    search_fields = ['query', 'response']
    ordering = ['-timestamp']
    raw_id_fields = ['conversation']
    filter_horizontal = ['chunks_used']

    def query_preview(self, obj):
        return obj.query[:100] + '...' if len(obj.query) > 100 else obj.query
    query_preview.short_description = 'Query'
