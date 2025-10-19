from django.db import models
from django.conf import settings
from pgvector.django import VectorField


class SourceDocument(models.Model):
    """Stores source documents for RAG"""
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    file_path = models.CharField(max_length=500)
    file_type = models.CharField(max_length=10)
    file_size = models.IntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_documents'
    )

    class Meta:
        db_table = 'source_documents'
        ordering = ['-upload_date']
        verbose_name = 'Source Document'
        verbose_name_plural = 'Source Documents'

    def __str__(self):
        return self.title


class DocumentChunk(models.Model):
    """Stores chunked text from documents with embeddings"""
    document = models.ForeignKey(SourceDocument, on_delete=models.CASCADE, related_name='chunks')
    content = models.TextField()
    chunk_index = models.IntegerField()
    metadata = models.JSONField(default=dict, blank=True)
    embedding = VectorField(dimensions=settings.EMBEDDING_DIMENSION)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'document_chunks'
        ordering = ['document', 'chunk_index']
        indexes = [
            models.Index(fields=['document', 'chunk_index']),
        ]
        verbose_name = 'Document Chunk'
        verbose_name_plural = 'Document Chunks'

    def __str__(self):
        return f"{self.document.title} - Chunk {self.chunk_index}"


class RAGQueryLog(models.Model):
    """Logs RAG queries and the chunks used for responses"""
    conversation = models.ForeignKey(
        'chatbot.Conversation',
        on_delete=models.CASCADE,
        related_name='rag_queries',
        null=True,
        blank=True
    )
    query = models.TextField()
    chunks_used = models.ManyToManyField(DocumentChunk, related_name='used_in_queries')
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    execution_time = models.FloatField(help_text="Time in seconds")

    class Meta:
        db_table = 'rag_query_logs'
        ordering = ['-timestamp']
        verbose_name = 'RAG Query Log'
        verbose_name_plural = 'RAG Query Logs'

    def __str__(self):
        return f"Query at {self.timestamp}: {self.query[:50]}"
