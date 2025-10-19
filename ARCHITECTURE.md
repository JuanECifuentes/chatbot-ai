# System Architecture Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  (Web Frontend, Mobile App, API Clients, CLI, Postman, etc.)   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/REST API
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      DJANGO REST API                             │
│                                                                   │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐  │
│  │   Chatbot API  │  │  RAG API       │  │  Admin Interface │  │
│  │  /api/chatbot/ │  │  /api/rag/     │  │    /admin/       │  │
│  └────────┬───────┘  └────────┬───────┘  └──────────────────┘  │
│           │                    │                                 │
└───────────┼────────────────────┼─────────────────────────────────┘
            │                    │
            │                    │
┌───────────▼────────────────────▼─────────────────────────────────┐
│                    APPLICATION LAYER                              │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  Chatbot App                              │   │
│  │  • User Management                                        │   │
│  │  • Conversation Management                                │   │
│  │  • Message Handling                                       │   │
│  └──────────────────┬───────────────────────────────────────┘   │
│                     │                                             │
│  ┌──────────────────▼───────────────────────────────────────┐   │
│  │                  RAG Engine App                           │   │
│  │  • Document Storage                                       │   │
│  │  • Chunk Management                                       │   │
│  │  • Query Logging                                          │   │
│  │  • RAG Service (Gemini Integration)                       │   │
│  └──────────────────┬───────────────────────────────────────┘   │
│                     │                                             │
│  ┌──────────────────▼───────────────────────────────────────┐   │
│  │           Document Processor App                          │   │
│  │  • PDF Parser                                             │   │
│  │  • DOCX Parser                                            │   │
│  │  • Text Normalizer                                        │   │
│  │  • Text Chunker                                           │   │
│  │  • Ingestion Service                                      │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                   │
└────────────────────────┬─────────────────┬──────────────────────┘
                         │                 │
                         │                 │
           ┌─────────────▼────┐    ┌──────▼───────────────┐
           │  PostgreSQL DB   │    │  Google Gemini API   │
           │                  │    │                      │
           │  • pgvector      │    │  • Gemini 2.5 Flash  │
           │  • Vector Search │    │  • Embedding Model   │
           └──────────────────┘    └──────────────────────┘
```

## Data Flow Diagram

### Document Upload Flow

```
┌──────────┐
│  Client  │
└────┬─────┘
     │ 1. Upload PDF/DOCX
     │
     ▼
┌─────────────────┐
│   RAG API       │
│ /documents/     │
└────┬────────────┘
     │ 2. Save file
     │
     ▼
┌──────────────────────┐
│ Document Processor   │
│  • Parse PDF/DOCX    │
│  • Extract metadata  │
│  • Normalize text    │
│  • Create chunks     │
└────┬─────────────────┘
     │ 3. Text chunks
     │
     ▼
┌──────────────────────┐
│  Gemini API          │
│  Generate embeddings │
└────┬─────────────────┘
     │ 4. Vector embeddings
     │
     ▼
┌──────────────────────┐
│  PostgreSQL          │
│  Store chunks +      │
│  embeddings (pgvector)│
└──────────────────────┘
```

### Chat Query Flow

```
┌──────────┐
│  Client  │
└────┬─────┘
     │ 1. Send message
     │
     ▼
┌─────────────────┐
│  Chatbot API    │
│ /chat/send_msg/ │
└────┬────────────┘
     │ 2. Create user message
     │
     ▼
┌──────────────────────┐
│  RAG Engine          │
│  • Generate query    │
│    embedding         │
└────┬─────────────────┘
     │ 3. Query embedding
     │
     ▼
┌──────────────────────┐
│  Gemini API          │
│  Generate embedding  │
└────┬─────────────────┘
     │ 4. Query vector
     │
     ▼
┌──────────────────────┐
│  PostgreSQL          │
│  Vector similarity   │
│  search (Top-K)      │
└────┬─────────────────┘
     │ 5. Similar chunks
     │
     ▼
┌──────────────────────┐
│  RAG Engine          │
│  • Build context     │
│  • Add history       │
└────┬─────────────────┘
     │ 6. Context + Query
     │
     ▼
┌──────────────────────┐
│  Gemini API          │
│  Generate response   │
└────┬─────────────────┘
     │ 7. AI Response
     │
     ▼
┌──────────────────────┐
│  Chatbot API         │
│  • Save assistant msg│
│  • Log query         │
└────┬─────────────────┘
     │ 8. Return response
     │
     ▼
┌──────────┐
│  Client  │
└──────────┘
```

## Database Schema

```
┌──────────────────┐         ┌─────────────────────┐
│      Users       │         │   Conversations     │
├──────────────────┤         ├─────────────────────┤
│ id (PK)          │◄────────┤ id (PK)             │
│ username         │ 1     * │ user_id (FK)        │
│ email            │         │ title               │
│ password         │         │ created_at          │
│ first_name       │         │ updated_at          │
│ last_name        │         └──────────┬──────────┘
│ created_at       │                    │
│ updated_at       │                    │ 1
└──────────────────┘                    │
                                        │ *
        ┌───────────────────────────────┘
        │
        ▼
┌─────────────────────┐         ┌──────────────────────┐
│     Messages        │         │   RAGQueryLogs       │
├─────────────────────┤         ├──────────────────────┤
│ id (PK)             │         │ id (PK)              │
│ conversation_id (FK)│◄────────┤ conversation_id (FK) │
│ sender (enum)       │ 1     * │ query                │
│ content             │         │ response             │
│ created_at          │         │ timestamp            │
└─────────────────────┘         │ execution_time       │
                                └──────────┬───────────┘
                                           │
                                           │ M
                                           │
                                           │ N
┌──────────────────────┐         ┌────────▼─────────────┐
│  SourceDocuments     │         │  DocumentChunks      │
├──────────────────────┤         ├──────────────────────┤
│ id (PK)              │◄────────┤ id (PK)              │
│ title                │ 1     * │ document_id (FK)     │
│ author               │         │ content              │
│ file_path            │         │ chunk_index          │
│ file_type            │         │ metadata (JSON)      │
│ file_size            │         │ embedding (VECTOR)   │
│ upload_date          │         │ created_at           │
│ metadata (JSON)      │         └──────────────────────┘
│ uploaded_by (FK)     │
└──────────────────────┘
```

## API Endpoint Structure

```
/api/
├── chatbot/
│   ├── conversations/
│   │   ├── GET    → List conversations
│   │   ├── POST   → Create conversation
│   │   ├── {id}/
│   │   │   ├── GET    → Get conversation details
│   │   │   ├── PATCH  → Update conversation
│   │   │   ├── DELETE → Delete conversation
│   │   │   └── messages/
│   │   │       └── GET → Get conversation messages
│   │   └── ...
│   └── chat/
│       └── send_message/
│           └── POST → Send message & get response
│
└── rag/
    ├── documents/
    │   ├── GET    → List documents
    │   ├── POST   → Create document
    │   ├── upload/
    │   │   └── POST → Upload & process document
    │   └── {id}/
    │       ├── GET    → Get document details
    │       ├── DELETE → Delete document
    │       ├── chunks/
    │       │   └── GET → Get document chunks
    │       └── reindex/
    │           └── POST → Reindex document
    ├── chunks/
    │   ├── GET → List all chunks
    │   └── {id}/
    │       └── GET → Get chunk details
    └── query-logs/
        ├── GET → List query logs
        └── {id}/
            └── GET → Get query log details
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────────┐
│                        Django Layer                          │
│                                                              │
│  ┌──────────────┐                                           │
│  │   Views      │ ◄──── Handles HTTP requests               │
│  └──────┬───────┘                                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐                                           │
│  │ Serializers  │ ◄──── Validates & transforms data         │
│  └──────┬───────┘                                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐                                           │
│  │   Models     │ ◄──── ORM data layer                      │
│  └──────┬───────┘                                           │
│         │                                                    │
└─────────┼──────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                      Service Layer                           │
│                                                              │
│  ┌──────────────┐     ┌──────────────┐    ┌──────────────┐ │
│  │ RAG Service  │     │  Document    │    │   Gemini     │ │
│  │              │────►│  Processor   │    │   Service    │ │
│  │ • Search     │     │              │    │              │ │
│  │ • Context    │     │ • Parse      │    │ • LLM        │ │
│  │ • Generate   │     │ • Chunk      │    │ • Embed      │ │
│  └──────────────┘     │ • Normalize  │    └──────────────┘ │
│                       └──────────────┘                      │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                              │
│                                                              │
│  ┌──────────────────────┐       ┌─────────────────────┐    │
│  │  PostgreSQL + pgvector│       │   Google Gemini API │    │
│  │                       │       │                     │    │
│  │  • Relational data    │       │  • LLM responses    │    │
│  │  • Vector embeddings  │       │  • Embeddings       │    │
│  │  • Similarity search  │       └─────────────────────┘    │
│  └──────────────────────┘                                   │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (Optional)                      │
│         React / Vue / Next.js / Mobile App                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ REST API / HTTP
                         │
┌────────────────────────▼────────────────────────────────────┐
│                      BACKEND                                 │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Django 4.2+ (Python Web Framework)                  │  │
│  │  • Django REST Framework (API)                        │  │
│  │  • django-cors-headers (CORS)                         │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Application Logic                                    │  │
│  │  • chatbot (Conversations)                            │  │
│  │  • rag_engine (RAG System)                            │  │
│  │  • document_processor (Document Processing)           │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────┬────────────────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ PostgreSQL   │  │ Google       │  │ File System  │
│ 12+          │  │ Gemini API   │  │              │
│              │  │              │  │ • PDF files  │
│ • pgvector   │  │ • 2.5 Flash  │  │ • DOCX files │
│ • ACID       │  │ • Embeddings │  │ • Media      │
│ • Indexes    │  │              │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
```

## Deployment Architecture (Production)

```
                    ┌──────────────┐
                    │  Load        │
                    │  Balancer    │
                    └──────┬───────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ Django   │    │ Django   │    │ Django   │
    │ Instance │    │ Instance │    │ Instance │
    └────┬─────┘    └────┬─────┘    └────┬─────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
  ┌──────────┐    ┌──────────┐    ┌──────────┐
  │PostgreSQL│    │  Redis   │    │  CDN     │
  │ Primary  │    │  Cache   │    │  Static  │
  └────┬─────┘    └──────────┘    └──────────┘
       │
       ▼
  ┌──────────┐
  │PostgreSQL│
  │ Replica  │
  └──────────┘
```

---

**This diagram shows the complete architecture of the RAG Chatbot system.**
