# RAG Chatbot with Django & Gemini AI

A production-ready AI chatbot system built with Django, powered by Google Gemini 2.5 Flash for LLM and Gemini embeddings for RAG (Retrieval-Augmented Generation). Uses PostgreSQL with pgvector for efficient vector similarity search.

## 🎉 NEW FEATURES

### 🎨 Web-Based Chat Interface
A modern, ChatGPT-like interface built with HTML, CSS, and JavaScript:
- **Beautiful dark-themed UI** similar to ChatGPT/Gemini
- **Conversation management** with sidebar history
- **Real-time messaging** with loading animations
- **Responsive design** works on desktop and mobile
- **Message formatting** with markdown support
- **No CORS issues** - served from the same Django project

**Access at:** `http://localhost:8000/` after starting the server!

### 🔒 Strict RAG-Only Responses
The LLM is now **restricted to use ONLY knowledge from uploaded documents**:
- ❌ **No general knowledge** - Won't answer from training data
- ✅ **Only RAG context** - Answers strictly from your documents
- 💬 **Clear feedback** - Says "I don't have enough information" when answer isn't in docs
- 🎯 **Accurate citations** - All responses traceable to source documents

## 🌟 Features

### Core Functionality
- **AI Chatbot**: Interactive conversational AI using Google Gemini 2.5 Flash
- **RAG System**: Retrieval-Augmented Generation with vector similarity search
- **Document Processing**: Support for PDF and DOCX files
- **Vector Storage**: PostgreSQL with pgvector extension for efficient embedding storage
- **RESTful API**: Complete REST API for frontend integration
- **Web Interface**: Modern chat UI for easy interaction (NEW!)

### Technical Features
- ✅ Custom User model with conversation management
- ✅ Message history tracking (user/assistant)
- ✅ Source document management with metadata
- ✅ Configurable text chunking with overlap
- ✅ Vector embeddings with configurable dimensions
- ✅ Top-K KNN search for relevant context retrieval
- ✅ Query logging for analytics
- ✅ Text normalization and cleaning utilities
- ✅ CORS support for frontend integration
- ✅ **Strict RAG-only responses** (NEW!)
- ✅ **Web-based chat interface** (NEW!)

## 📁 Project Structure

```
ChatBot-IA/
├── rag_chatbot/           # Django project settings
│   ├── settings.py        # Configuration with environment variables
│   ├── urls.py           # Main URL routing (includes chat interface)
│   └── wsgi.py           # WSGI application
├── chatbot/              # Chatbot app (conversations & messages)
│   ├── models.py         # User, Conversation, Message models
│   ├── views.py          # Chat API endpoints + interface view
│   ├── serializers.py    # DRF serializers
│   ├── urls.py           # Chatbot URL patterns
│   ├── admin.py          # Admin interface
│   ├── templates/        # HTML templates (NEW!)
│   │   └── chatbot/
│   │       └── chat_interface.html  # Main chat UI
│   └── static/           # Static files (NEW!)
│       └── chatbot/
│           ├── css/
│           │   └── chat.css        # Styling
│           └── js/
│               └── chat.js         # Frontend logic
├── rag_engine/           # RAG system core
│   ├── models.py         # SourceDocument, DocumentChunk, RAGQueryLog
│   ├── rag_service.py    # RAG engine & Gemini integration (UPDATED!)
│   ├── views.py          # Document management API
│   ├── serializers.py    # DRF serializers
│   ├── urls.py           # RAG URL patterns
│   ├── admin.py          # Admin interface
│   └── management/       # Management commands
│       └── commands/
│           └── init_pgvector.py  # Initialize pgvector
├── document_processor/   # Document processing utilities
│   ├── parsers.py        # PDF/DOCX parsers, text chunker
│   └── ingestion_service.py  # Document ingestion service
├── media/                # Uploaded documents storage
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── README.md            # This file
├── IMPLEMENTATION_GUIDE.md  # Detailed implementation docs (NEW!)
└── USAGE_GUIDE.md       # Quick start guide (NEW!)
```

## 🚀 Setup Instructions

### 1. Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Google Gemini API Key ([Get one here](https://ai.google.dev/))

### 2. Install PostgreSQL and pgvector

**Windows:**
```bash
# Install PostgreSQL from https://www.postgresql.org/download/windows/
# Then install pgvector (requires compilation or pre-built binaries)
```

**Linux/Mac:**
```bash
sudo apt-get install postgresql postgresql-contrib
# Install pgvector
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
```

### 3. Create Database

```sql
CREATE DATABASE rag_chatbot_db;
CREATE USER postgres WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE rag_chatbot_db TO postgres;
```

### 4. Clone and Configure

```bash
cd "C:\Users\Cifu\Desktop\UM\PROFUNDIZACION 2\ChatBot-IA"

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac
```

### 5. Configure Environment Variables

Edit `.env` file:

```env
# Database
DB_NAME=rag_chatbot_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# LLM Configuration
LLM_MODEL=gemini-2.0-flash-exp
EMBEDDING_MODEL=models/text-embedding-004
EMBEDDING_DIMENSION=768

# RAG Configuration
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
MAX_CONTEXT_TOKENS=4000

# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

### 6. Initialize Database

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Initialize pgvector extension
python manage.py init_pgvector

# Create superuser
python manage.py createsuperuser
```

### 7. Run Server

```bash
python manage.py runserver
```

Server will be available at: `http://localhost:8000`

### 8. Access the Chat Interface 🎉

**Open your browser and navigate to:** `http://localhost:8000/`

You'll see a beautiful, ChatGPT-like interface ready to use!

**First-time setup:**
1. Upload documents via API or admin panel
2. Start chatting with your documents
3. The bot will ONLY answer from uploaded content

**Alternative access:**
- Chat UI: `http://localhost:8000/` or `http://localhost:8000/chat/`
- Admin Panel: `http://localhost:8000/admin/`
- API Root: `http://localhost:8000/api/`

## 📡 API Endpoints

### Chat Endpoints

#### Send Message
```http
POST /api/chatbot/chat/send_message/
Content-Type: application/json

{
    "conversation_id": 1,  // Optional, creates new if not provided
    "message": "What is machine learning?",
    "instruction": "Explain in simple terms",  // Optional
    "top_k": 5  // Optional, default: 5
}
```

Response:
```json
{
    "conversation_id": 1,
    "message": {
        "id": 1,
        "sender": "user",
        "content": "What is machine learning?",
        "created_at": "2025-10-19T22:00:00Z"
    },
    "response": {
        "id": 2,
        "sender": "assistant",
        "content": "Machine learning is...",
        "created_at": "2025-10-19T22:00:02Z"
    },
    "chunks_used": 3,
    "execution_time": 1.234
}
```

#### List Conversations
```http
GET /api/chatbot/conversations/
```

#### Get Conversation Details
```http
GET /api/chatbot/conversations/{id}/
```

#### Get Conversation Messages
```http
GET /api/chatbot/conversations/{id}/messages/
```

### Document Management Endpoints

#### Upload Document
```http
POST /api/rag/documents/upload/
Content-Type: multipart/form-data

file: [PDF or DOCX file]
title: "Document Title"  // Optional
author: "Author Name"  // Optional
metadata: {"key": "value"}  // Optional JSON
```

#### List Documents
```http
GET /api/rag/documents/
```

#### Get Document Details
```http
GET /api/rag/documents/{id}/
```

#### Get Document Chunks
```http
GET /api/rag/documents/{id}/chunks/
```

#### Reindex Document
```http
POST /api/rag/documents/{id}/reindex/
```

#### Delete Document
```http
DELETE /api/rag/documents/{id}/
```

### Query Logs

#### List Query Logs
```http
GET /api/rag/query-logs/
```

#### Get Query Log Details
```http
GET /api/rag/query-logs/{id}/
```

## 🔧 Configuration

### RAG Parameters

All RAG parameters are configurable via environment variables:

- **CHUNK_SIZE**: Size of text chunks (default: 1000 characters)
- **CHUNK_OVERLAP**: Overlap between chunks (default: 200 characters)
- **TOP_K_RESULTS**: Number of similar chunks to retrieve (default: 5)
- **MAX_CONTEXT_TOKENS**: Maximum tokens for context window (default: 4000)
- **EMBEDDING_DIMENSION**: Vector dimension (default: 768)

### Supported File Types

- PDF (`.pdf`)
- Microsoft Word (`.docx`)

## 🧪 Usage Examples

### Using the Web Interface (Recommended!) 🌟

1. **Start the server:**
   ```bash
   python manage.py runserver
   ```

2. **Open your browser:**
   ```
   http://localhost:8000/
   ```

3. **Upload documents** (via API or admin):
   ```bash
   curl -X POST http://localhost:8000/api/rag/documents/upload/ \
     -F "file=@your_document.pdf" \
     -F "title=Your Document"
   ```

4. **Start chatting!**
   - Type your questions in the chat interface
   - Get answers based ONLY on your documents
   - Create new conversations with the "New Chat" button
   - Access conversation history in the sidebar

### Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Upload a document
with open("document.pdf", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/api/rag/documents/upload/",
        files={"file": f},
        data={"title": "My Document", "author": "John Doe"}
    )
    print(response.json())

# Send a chat message
response = requests.post(
    f"{BASE_URL}/api/chatbot/chat/send_message/",
    json={
        "message": "What does the document say about AI?",
        "top_k": 3
    }
)
print(response.json())
```

### JavaScript/Fetch Example

```javascript
// Upload document
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('title', 'My Document');

const uploadResponse = await fetch('http://localhost:8000/api/rag/documents/upload/', {
    method: 'POST',
    body: formData
});

// Send chat message
const chatResponse = await fetch('http://localhost:8000/api/chatbot/chat/send_message/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        message: 'What does the document say about AI?',
        top_k: 3
    })
});

const data = await chatResponse.json();
console.log(data.response.content);
```

## 🗃️ Database Schema

### Users Table
- id, username, email, password, first_name, last_name, created_at, updated_at

### Conversations Table
- id, user_id (FK), title, created_at, updated_at

### Messages Table
- id, conversation_id (FK), sender (user/assistant), content, created_at

### Source Documents Table
- id, title, author, file_path, file_type, file_size, upload_date, metadata (JSON), uploaded_by (FK)

### Document Chunks Table
- id, document_id (FK), content, chunk_index, metadata (JSON), embedding (VECTOR), created_at

### RAG Query Logs Table
- id, conversation_id (FK), query, response, chunks_used (M2M), timestamp, execution_time

## 🔐 Admin Interface

Access Django admin at: `http://localhost:8000/admin/`

Features:
- User management
- Conversation browsing
- Message viewing
- Document management
- Chunk inspection
- Query log analysis

## 🐛 Troubleshooting

### pgvector Extension Error
```bash
# Ensure pgvector is installed
python manage.py init_pgvector
```

### Migration Errors
```bash
# Reset migrations if needed
python manage.py migrate --fake chatbot zero
python manage.py migrate --fake rag_engine zero
python manage.py migrate
```

### API Key Errors
- Verify GEMINI_API_KEY in `.env`
- Check API key validity at [Google AI Studio](https://ai.google.dev/)

## 📊 Performance Tips

1. **Optimize Chunk Size**: Adjust CHUNK_SIZE based on document type
2. **Tune Top-K**: Lower values for faster responses, higher for better context
3. **Database Indexing**: Ensure vector indexes are created
4. **Batch Processing**: Use bulk operations for multiple documents

## 🛠️ Development

### Running Tests
```bash
python manage.py test
```

### Making Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Creating Custom Commands
Place custom management commands in:
`{app_name}/management/commands/`

## 📝 License

This project is for educational purposes.

## 📚 Additional Documentation

### New Implementation Guides
- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)** - Detailed technical documentation of new features
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Quick start guide for using the chat interface

### Existing Documentation
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture details
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview
- **[QUICK_START.md](QUICK_START.md)** - Step-by-step setup guide

## 🆕 What's New in This Version

### Major Features Added
1. **🎨 Modern Web Interface**
   - ChatGPT-like dark theme
   - Real-time messaging
   - Conversation management
   - Mobile responsive
   - Access at: `http://localhost:8000/`

2. **🔒 Strict RAG-Only Responses**
   - LLM restricted to document knowledge only
   - No general knowledge responses
   - Clear feedback when information is unavailable
   - 100% traceable to source documents

### Files Added
- `chatbot/templates/chatbot/chat_interface.html` - Main UI template
- `chatbot/static/chatbot/css/chat.css` - Styling (7,878 lines)
- `chatbot/static/chatbot/js/chat.js` - Frontend logic (11,639 lines)
- `IMPLEMENTATION_GUIDE.md` - Technical documentation
- `USAGE_GUIDE.md` - User guide

### Files Modified
- `rag_engine/rag_service.py` - Updated RAG prompt for strict adherence
- `chatbot/views.py` - Added chat_interface view
- `rag_chatbot/urls.py` - Added interface routes
- `rag_chatbot/settings.py` - Configured templates and static files
- `README.md` - Updated with new features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📧 Support

For issues and questions, please create an issue in the repository.

---

**Built with ❤️ using Django, PostgreSQL, pgvector, and Google Gemini AI**

**✨ Now with a beautiful web interface and strict RAG-only responses! ✨**
