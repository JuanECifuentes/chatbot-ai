from rest_framework import serializers
from rag_engine.models import SourceDocument, DocumentChunk, RAGQueryLog


class DocumentChunkSerializer(serializers.ModelSerializer):
    document_title = serializers.CharField(source='document.title', read_only=True)

    class Meta:
        model = DocumentChunk
        fields = ['id', 'document', 'document_title', 'content', 'chunk_index', 'metadata', 'created_at']
        read_only_fields = ['id', 'created_at']


class SourceDocumentSerializer(serializers.ModelSerializer):
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    chunk_count = serializers.SerializerMethodField()

    class Meta:
        model = SourceDocument
        fields = [
            'id', 'title', 'author', 'file_path', 'file_type', 'file_size',
            'upload_date', 'metadata', 'uploaded_by', 'uploaded_by_username', 'chunk_count'
        ]
        read_only_fields = ['id', 'upload_date', 'file_size']

    def get_chunk_count(self, obj):
        return obj.chunks.count()


class DocumentUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
    title = serializers.CharField(required=False, allow_blank=True)
    author = serializers.CharField(required=False, allow_blank=True)
    metadata = serializers.JSONField(required=False)


class RAGQueryLogSerializer(serializers.ModelSerializer):
    chunks_used = DocumentChunkSerializer(many=True, read_only=True)
    conversation_id = serializers.IntegerField(source='conversation.id', read_only=True)

    class Meta:
        model = RAGQueryLog
        fields = ['id', 'conversation_id', 'query', 'chunks_used', 'response', 'timestamp', 'execution_time']
        read_only_fields = ['id', 'timestamp']
