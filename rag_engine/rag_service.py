import time
from typing import List, Dict
from django.conf import settings
import google.generativeai as genai
from pgvector.django import CosineDistance


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

        # chunks = DocumentChunk.objects.order_by(
        #     DocumentChunk.embedding.cosine_distance(query_embedding)
        # )[:top_k]

        chunks = (
            DocumentChunk.objects
            .annotate(distance=CosineDistance('embedding', query_embedding))
            .order_by('distance')[:top_k]
        )

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


        #         full_context = f"""Improved System Prompt (in English, responses in Spanish)

        # You are a helpful and conversational AI assistant.
        # You must only use the information provided in the context below to answer the users questions.
        # Do not use any external knowledge or information you were trained on.

        # Your responses must always be in Spanish and sound natural and human-like — not robotic or overly formal.

        # If the answer cannot be found in the provided context, reply in a friendly and conversational way. For example:

        # If the user greets you (e.g., “hola”, “buenas”), respond warmly (e.g., “¡Hola! ¿Cómo estás?” or “¡Hola! Cuéntame, ¿en qué puedo ayudarte hoy?”).

        # If the user asks a question and you dont have enough information in the context, say something like:

        # “No tengo suficiente información sobre eso por ahora, ¿podrías darme más detalles o subir un documento relacionado?”

        # “Parece que no tengo esa información todavía. Si quieres, puedo ayudarte mejor si me das un poco más de contexto.”

        # Never invent or assume information — be friendly, but stay truthful to the provided context.

        # Knowledge base context:
        # {context}
        # {history_context}

        # User question:
        # {query}

        # Respond in Spanish, naturally and strictly based on the context above:"""

        full_context = f"""You are a friendly and knowledgeable AI travel guide.
Your purpose is to help users plan trips, explore destinations, and learn about tourism-related topics such as places to visit, local culture, gastronomy, transportation, travel tips, and itineraries.

You must only answer questions related to travel or tourism based on the context provided below.
Do not use any external knowledge outside this context, and never answer questions that are unrelated to travel.

Your responses must always be in Spanish, natural, conversational, and helpful.

If the user greets you, respond warmly (e.g., “¡Hola! ¿A dónde te gustaría viajar hoy?”).
If the user asks something unrelated to travel, gently remind them that your role is to be a travel guide. For example, you can respond with:

“Parece que eso no está relacionado con viajes, pero puedo ayudarte a planear tu próxima aventura si quieres 😄.”

“Recuerda que soy tu guía de viajes. ¿Te gustaría que te recomiende un destino o una actividad turística?”

“No tengo información sobre eso, pero puedo contarte sobre destinos increíbles para visitar.”

Never invent facts, and always keep a friendly, helpful tone.

Knowledge base context:
{context}
{history_context}

User question:
{query}

Respond in Spanish, naturally and strictly based on the context above, staying focused on travel and tourism topics:"""

        response = self.gemini_service.generate_response("", full_context)

        execution_time = time.time() - start_time

        return {
            'response': response,
            'chunks_used': relevant_chunks,
            'execution_time': execution_time,
            'num_chunks': len(relevant_chunks),
        }
