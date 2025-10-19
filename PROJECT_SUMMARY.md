# Project Summary: RAG Chatbot with Django & Gemini AI

## Project Overview

This is a complete, production-ready AI chatbot system built with Django that implements Retrieval-Augmented Generation (RAG) using Google Gemini AI models. The system allows users to upload documents (PDF/DOCX), automatically processes them into searchable chunks with vector embeddings, and provides an intelligent chatbot that answers questions based on the uploaded content.

## Key Technologies

- **Backend Framework**: Django 4.2+ with Django REST Framework
- **Database**: PostgreSQL with pgvector extension for vector similarity search
- **AI/ML**: 
  - Google Gemini 2.5 Flash (LLM for responses)
  - Gemini Embedding Model (text-embedding-004) for vector embeddings
- **Document Processing**: PyPDF for PDFs, python-docx for Word documents
- **API**: RESTful API with full CRUD operations

## Architecture

### Three-App Modular Design

1. **chatbot** - User interactions and conversation management
   - Custom User model
   - Conversation tracking
   - Message history (user/assistant distinction)
   
2. **rag_engine** - RAG system core
   - Document storage and management
   - Vector chunk storage with embeddings
   - Query logging and analytics
   - RAG service with Gemini integration
   
3. **document_processor** - Document processing utilities
   - PDF/DOCX parsers
   - Text normalization and cleaning
   - Configurable chunking with overlap
   - Document ingestion pipeline

## Database Schema

### Tables

1. **users** - Custom user model extending Django's AbstractUser
2. **conversations** - Chat conversation sessions
3. **messages** - Individual messages with sender type (user/assistant)
4. **source_documents** - Uploaded documents with metadata
5. **document_chunks** - Text chunks with VECTOR embeddings
6. **rag_query_logs** - Query history with chunks used and execution time

### Vector Support

- Uses pgvector extension for efficient similarity search
- Configurable embedding dimensions (default: 768)
- Cosine distance similarity for chunk retrieval

## Features Implemented

### Core Features

✅ **Document Upload & Processing**
- Support for PDF and DOCX files
- Automatic text extraction with metadata
- Configurable chunking (size and overlap)
- Vector embedding generation
- Bulk chunk creation for efficiency

✅ **RAG System**
- Vector similarity search using pgvector
- Top-K KNN retrieval (configurable)
- Context window management (max tokens)
- Conversation history support
- Query logging for analytics

✅ **Chatbot**
- Conversational AI using Gemini 2.5 Flash
- Context-aware responses
- Conversation threading
- Message history tracking
- Custom instructions support

✅ **API Endpoints**
- RESTful API with DRF
- Document CRUD operations
- Chat interface
- Conversation management
- Query log viewing
- Document reindexing

✅ **Text Processing**
- Accent removal and normalization
- Text cleaning and whitespace handling
- Smart chunking with sentence boundaries
- Metadata extraction from documents

### Configuration

All parameters configurable via environment variables:
- Database credentials
- Gemini API key
- Model selection (LLM and embedding)
- Chunk size and overlap
- Top-K results
- Max context tokens
- Embedding dimensions
- CORS settings

## API Endpoints Summary

### Chatbot API (`/api/chatbot/`)
- `POST /chat/send_message/` - Send message and get AI response
- `GET /conversations/` - List all conversations
- `GET /conversations/{id}/` - Get conversation details
- `GET /conversations/{id}/messages/` - Get conversation messages
- `POST /conversations/` - Create new conversation
- `PATCH /conversations/{id}/` - Update conversation
- `DELETE /conversations/{id}/` - Delete conversation

### RAG API (`/api/rag/`)
- `POST /documents/upload/` - Upload and process document
- `GET /documents/` - List all documents
- `GET /documents/{id}/` - Get document details
- `GET /documents/{id}/chunks/` - Get document chunks
- `POST /documents/{id}/reindex/` - Reindex document
- `DELETE /documents/{id}/` - Delete document
- `GET /chunks/` - List all chunks
- `GET /chunks/{id}/` - Get chunk details
- `GET /query-logs/` - List query logs
- `GET /query-logs/{id}/` - Get query log details

## File Structure

```
ChatBot-IA/
├── chatbot/                    # Conversation & messaging app
│   ├── models.py              # User, Conversation, Message
│   ├── views.py               # Chat API views
│   ├── serializers.py         # DRF serializers
│   ├── urls.py                # URL routing
│   └── admin.py               # Admin interface
│
├── rag_engine/                # RAG system core
│   ├── models.py              # Document, Chunk, QueryLog
│   ├── rag_service.py         # RAG logic & Gemini integration
│   ├── views.py               # Document API views
│   ├── serializers.py         # DRF serializers
│   ├── urls.py                # URL routing
│   ├── admin.py               # Admin interface
│   └── management/commands/
│       └── init_pgvector.py   # Database initialization
│
├── document_processor/        # Document processing
│   ├── parsers.py             # PDF/DOCX parsers, chunker
│   └── ingestion_service.py   # Document ingestion pipeline
│
├── rag_chatbot/               # Django project
│   ├── settings.py            # Configuration
│   └── urls.py                # Main routing
│
├── media/                     # Uploaded documents
├── requirements.txt           # Dependencies
├── .env.example              # Environment template
├── README.md                 # Main documentation
├── API_DOCUMENTATION.md      # API reference
├── QUICK_START.md            # Quick start guide
├── PROJECT_SUMMARY.md        # This file
├── test_installation.py      # Installation test script
├── setup.bat                 # Windows setup script
└── setup.sh                  # Linux/Mac setup script
```

## Setup Process

1. **Install PostgreSQL** with pgvector extension
2. **Create database** (rag_chatbot_db)
3. **Clone project** and install dependencies
4. **Configure .env** with credentials and API keys
5. **Run migrations** to create tables
6. **Initialize pgvector** extension
7. **Create superuser** for admin access
8. **Start server** and begin using

## Usage Flow

1. **Upload Documents** → System chunks and embeds them
2. **Ask Questions** → RAG retrieves relevant chunks
3. **Get Responses** → Gemini generates contextual answers
4. **View History** → Track conversations and queries
5. **Manage Documents** → Update or remove as needed

## Performance Considerations

- Bulk chunk creation for efficiency
- Vector indexing for fast similarity search
- Configurable context window to manage token usage
- Query logging for performance monitoring
- Efficient database queries with select_related/prefetch_related

## Security Features

- Environment-based configuration
- .gitignore for sensitive files
- CORS configuration for frontend integration
- Custom user model for extensibility
- SQL injection protection via Django ORM

## Extensibility

The modular design allows easy extension:
- Add new document types (implement parser)
- Change LLM provider (modify rag_service)
- Add authentication (JWT, OAuth)
- Implement caching (Redis)
- Add real-time features (WebSockets)
- Deploy with Docker
- Scale with load balancing

## Testing

- Installation test script provided
- Manual API testing with cURL/Postman
- Admin interface for data inspection
- Query logs for debugging

## Documentation

- **README.md** - Complete setup and overview
- **API_DOCUMENTATION.md** - Full API reference with examples
- **QUICK_START.md** - Step-by-step beginner guide
- **PROJECT_SUMMARY.md** - This architectural overview

## Development Best Practices

- Environment variables for configuration
- Modular app design
- DRF serializers for validation
- Django admin for management
- Proper model relationships
- Efficient database queries
- Error handling and logging
- Clean code structure

## Production Readiness

For production deployment:
1. Set DEBUG=False
2. Configure ALLOWED_HOSTS
3. Use environment secrets management
4. Set up proper CORS policies
5. Implement rate limiting
6. Add authentication/authorization
7. Use PostgreSQL connection pooling
8. Set up monitoring and logging
9. Configure static file serving
10. Use HTTPS

## Future Enhancements

Potential improvements:
- User authentication with JWT
- Role-based access control
- Document sharing between users
- Advanced search filters
- Batch document upload
- Document categories/tags
- Citation tracking in responses
- Multi-language support
- Real-time chat with WebSockets
- Mobile app integration
- Analytics dashboard
- Export conversations
- Custom LLM fine-tuning

## Dependencies

Key packages:
- Django 4.2+
- djangorestframework
- psycopg2-binary (PostgreSQL)
- python-dotenv (environment)
- google-generativeai (Gemini)
- pypdf (PDF parsing)
- python-docx (DOCX parsing)
- pgvector (vector operations)
- django-cors-headers (CORS)

## License & Credits

Educational project demonstrating:
- RAG implementation
- Django REST API design
- Vector database usage
- LLM integration
- Document processing

Built with Django, PostgreSQL, pgvector, and Google Gemini AI.

---

**Project Status**: ✅ Complete and ready for use

**Created**: October 2025

**Python Version**: 3.8+

**Django Version**: 4.2+
