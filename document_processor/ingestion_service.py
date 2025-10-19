import os
from typing import Dict, List
from django.conf import settings
from django.core.files.storage import default_storage
from rag_engine.models import SourceDocument, DocumentChunk
from rag_engine.rag_service import GeminiService
from document_processor.parsers import DocumentParser, TextNormalizer, TextChunker


class DocumentIngestionService:
    """Service for ingesting documents into the RAG system"""

    def __init__(self):
        self.gemini_service = GeminiService()
        self.parser = DocumentParser()
        self.normalizer = TextNormalizer()
        self.chunker = TextChunker()
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP

    def ingest_document(
        self,
        file_path: str,
        title: str = None,
        author: str = None,
        user=None,
        additional_metadata: Dict = None
    ) -> SourceDocument:
        """Ingest a document into the RAG system"""
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            text, doc_metadata = self.parser.parse_pdf(file_path)
        elif file_extension == '.docx':
            text, doc_metadata = self.parser.parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

        basic_metadata = self.parser.extract_metadata(file_path, file_extension)
        
        if additional_metadata:
            doc_metadata.update(additional_metadata)
        doc_metadata.update(basic_metadata)

        if not title:
            title = doc_metadata.get('title') or os.path.basename(file_path)
        
        if not author:
            author = doc_metadata.get('author', '')

        source_document = SourceDocument.objects.create(
            title=title,
            author=author,
            file_path=file_path,
            file_type=file_extension,
            file_size=basic_metadata['file_size'],
            metadata=doc_metadata,
            uploaded_by=user
        )

        cleaned_text = self.normalizer.process_text(text, normalize=False)
        
        chunks = self.chunker.chunk_text(
            cleaned_text,
            self.chunk_size,
            self.chunk_overlap
        )

        self._create_chunks_with_embeddings(source_document, chunks, doc_metadata)

        return source_document

    def _create_chunks_with_embeddings(
        self,
        document: SourceDocument,
        chunks: List[Dict],
        doc_metadata: Dict
    ):
        """Create document chunks with embeddings"""
        chunk_objects = []

        for chunk_data in chunks:
            embedding = self.gemini_service.generate_embedding(chunk_data['content'])
            
            chunk_metadata = {
                'title': document.title,
                'author': document.author,
                'start_position': chunk_data['start_position'],
                'end_position': chunk_data['end_position'],
            }

            chunk = DocumentChunk(
                document=document,
                content=chunk_data['content'],
                chunk_index=chunk_data['chunk_index'],
                metadata=chunk_metadata,
                embedding=embedding
            )
            chunk_objects.append(chunk)

        DocumentChunk.objects.bulk_create(chunk_objects)

    def delete_document(self, document_id: int):
        """Delete a document and all its chunks"""
        try:
            document = SourceDocument.objects.get(id=document_id)
            
            if os.path.exists(document.file_path):
                os.remove(document.file_path)
            
            document.delete()
            
            return True
        except SourceDocument.DoesNotExist:
            return False

    def reindex_document(self, document_id: int) -> SourceDocument:
        """Reindex a document (regenerate chunks and embeddings)"""
        document = SourceDocument.objects.get(id=document_id)
        
        document.chunks.all().delete()
        
        file_extension = document.file_type
        
        if file_extension == '.pdf':
            text, _ = self.parser.parse_pdf(document.file_path)
        elif file_extension == '.docx':
            text, _ = self.parser.parse_docx(document.file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

        cleaned_text = self.normalizer.process_text(text, normalize=False)
        
        chunks = self.chunker.chunk_text(
            cleaned_text,
            self.chunk_size,
            self.chunk_overlap
        )

        self._create_chunks_with_embeddings(document, chunks, document.metadata)

        return document
