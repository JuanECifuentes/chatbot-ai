import time
from typing import List, Dict
from django.conf import settings
import google.generativeai as genai


class GeminiService:
    """Service for interacting with Google Gemini API"""

    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.llm_model = genai.GenerativeModel(settings.LLM_MODEL)
        self.embedding_model = settings.EMBEDDING_MODEL

    def generate_response(self, prompt: str, context: str = "") -> str:
        """Generate a response using Gemini LLM"""
        try:
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            response = self.llm_model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings using Gemini embedding model"""
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            raise Exception(f"Error generating embedding: {str(e)}")

    def generate_query_embedding(self, query: str) -> List[float]:
        """Generate embeddings for search queries"""
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=query,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            raise Exception(f"Error generating query embedding: {str(e)}")


class RAGEngine:
    """RAG engine for retrieving relevant documents and generating responses"""

    def __init__(self):
        self.gemini_service = GeminiService()
        self.top_k = settings.TOP_K_RESULTS
        self.max_context_tokens = settings.MAX_CONTEXT_TOKENS

    def search_similar_chunks(self, query_embedding: List[float], top_k: int = None) -> List:
        """Search for similar document chunks using vector similarity"""
        from rag_engine.models import DocumentChunk

        if top_k is None:
            top_k = self.top_k

        chunks = DocumentChunk.objects.order_by(
            DocumentChunk.embedding.cosine_distance(query_embedding)
        )[:top_k]

        return list(chunks)

    def build_context(self, chunks: List, max_tokens: int = None) -> str:
        """Build context from retrieved chunks"""
        if max_tokens is None:
            max_tokens = self.max_context_tokens

        context_parts = []
        total_length = 0

        for chunk in chunks:
            chunk_text = f"Source: {chunk.document.title}\n{chunk.content}\n"
            chunk_length = len(chunk_text.split())

            if total_length + chunk_length > max_tokens:
                break

            context_parts.append(chunk_text)
            total_length += chunk_length

        return "\n---\n".join(context_parts)

    def generate_rag_response(
        self,
        query: str,
        conversation_history: List[Dict] = None,
        top_k: int = None
    ) -> Dict:
        """Generate response using RAG"""
        start_time = time.time()

        query_embedding = self.gemini_service.generate_query_embedding(query)
        relevant_chunks = self.search_similar_chunks(query_embedding, top_k)

        context = self.build_context(relevant_chunks)

        history_context = ""
        if conversation_history:
            history_parts = []
            for msg in conversation_history[-5:]:
                role = "User" if msg['sender'] == 'user' else "Assistant"
                history_parts.append(f"{role}: {msg['content']}")
            history_context = "\nConversation History:\n" + "\n".join(history_parts) + "\n"

        full_context = f"""You are a helpful AI assistant. Use the following context to answer the user's question.
If the answer cannot be found in the context, say so clearly.

Context from knowledge base:
{context}
{history_context}
User Question: {query}

Answer:"""

        response = self.gemini_service.generate_response("", full_context)

        execution_time = time.time() - start_time

        return {
            'response': response,
            'chunks_used': relevant_chunks,
            'execution_time': execution_time,
            'num_chunks': len(relevant_chunks),
        }
