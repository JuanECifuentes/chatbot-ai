# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API does not require authentication for development. In production, you should implement token-based authentication.

---

## Chatbot API

### 1. Send Message to Chatbot

**Endpoint:** `POST /api/chatbot/chat/send_message/`

**Description:** Send a message to the chatbot and receive an AI-generated response using RAG.

**Request Body:**
```json
{
    "conversation_id": 1,           // Optional: ID of existing conversation
    "message": "Your question here", // Required: User's message
    "instruction": "Additional context", // Optional: System instruction
    "top_k": 5                       // Optional: Number of chunks to retrieve (default: 5)
}
```

**Response:**
```json
{
    "conversation_id": 1,
    "message": {
        "id": 123,
        "conversation": 1,
        "sender": "user",
        "content": "Your question here",
        "created_at": "2025-10-19T22:00:00Z"
    },
    "response": {
        "id": 124,
        "conversation": 1,
        "sender": "assistant",
        "content": "AI generated response based on RAG context",
        "created_at": "2025-10-19T22:00:02Z"
    },
    "chunks_used": 3,
    "execution_time": 1.234
}
```

**Status Codes:**
- 200: Success
- 400: Bad Request (invalid input)
- 404: Conversation not found

---

### 2. List Conversations

**Endpoint:** `GET /api/chatbot/conversations/`

**Description:** Get list of all conversations.

**Response:**
```json
[
    {
        "id": 1,
        "title": "Conversation about AI",
        "message_count": 10,
        "last_message": {
            "sender": "assistant",
            "content": "That's a great question...",
            "created_at": "2025-10-19T22:00:00Z"
        },
        "created_at": "2025-10-19T20:00:00Z",
        "updated_at": "2025-10-19T22:00:00Z"
    }
]
```

---

### 3. Get Conversation Details

**Endpoint:** `GET /api/chatbot/conversations/{id}/`

**Description:** Get detailed information about a specific conversation including all messages.

**Response:**
```json
{
    "id": 1,
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "created_at": "2025-10-19T10:00:00Z"
    },
    "title": "Conversation about AI",
    "messages": [
        {
            "id": 1,
            "conversation": 1,
            "sender": "user",
            "content": "What is AI?",
            "created_at": "2025-10-19T20:00:00Z"
        },
        {
            "id": 2,
            "conversation": 1,
            "sender": "assistant",
            "content": "AI stands for Artificial Intelligence...",
            "created_at": "2025-10-19T20:00:02Z"
        }
    ],
    "created_at": "2025-10-19T20:00:00Z",
    "updated_at": "2025-10-19T22:00:00Z"
}
```

---

### 4. Get Conversation Messages

**Endpoint:** `GET /api/chatbot/conversations/{id}/messages/`

**Description:** Get all messages from a specific conversation.

**Response:**
```json
[
    {
        "id": 1,
        "conversation": 1,
        "sender": "user",
        "content": "What is AI?",
        "created_at": "2025-10-19T20:00:00Z"
    },
    {
        "id": 2,
        "conversation": 1,
        "sender": "assistant",
        "content": "AI stands for Artificial Intelligence...",
        "created_at": "2025-10-19T20:00:02Z"
    }
]
```

---

### 5. Create Conversation

**Endpoint:** `POST /api/chatbot/conversations/`

**Request Body:**
```json
{
    "title": "New Conversation"  // Optional
}
```

**Response:**
```json
{
    "id": 2,
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com"
    },
    "title": "New Conversation",
    "messages": [],
    "created_at": "2025-10-19T22:30:00Z",
    "updated_at": "2025-10-19T22:30:00Z"
}
```

---

### 6. Update Conversation

**Endpoint:** `PATCH /api/chatbot/conversations/{id}/`

**Request Body:**
```json
{
    "title": "Updated Title"
}
```

---

### 7. Delete Conversation

**Endpoint:** `DELETE /api/chatbot/conversations/{id}/`

**Status Codes:**
- 204: Successfully deleted

---

## RAG Engine API

### 1. Upload Document

**Endpoint:** `POST /api/rag/documents/upload/`

**Description:** Upload and process a document (PDF or DOCX) for RAG.

**Content-Type:** `multipart/form-data`

**Form Data:**
- `file`: (file) PDF or DOCX file [Required]
- `title`: (string) Document title [Optional]
- `author`: (string) Author name [Optional]
- `metadata`: (JSON string) Additional metadata [Optional]

**Example using cURL:**
```bash
curl -X POST http://localhost:8000/api/rag/documents/upload/ \
  -F "file=@document.pdf" \
  -F "title=My Document" \
  -F "author=John Doe" \
  -F 'metadata={"department":"IT","category":"research"}'
```

**Response:**
```json
{
    "id": 1,
    "title": "My Document",
    "author": "John Doe",
    "file_path": "/media/document.pdf",
    "file_type": ".pdf",
    "file_size": 1048576,
    "upload_date": "2025-10-19T22:00:00Z",
    "metadata": {
        "department": "IT",
        "category": "research",
        "num_pages": 10
    },
    "uploaded_by": 1,
    "uploaded_by_username": "john_doe",
    "chunk_count": 25
}
```

**Status Codes:**
- 201: Successfully created
- 400: Bad Request (invalid file type or missing file)
- 500: Server error during processing

---

### 2. List Documents

**Endpoint:** `GET /api/rag/documents/`

**Description:** Get list of all uploaded documents.

**Response:**
```json
[
    {
        "id": 1,
        "title": "Machine Learning Basics",
        "author": "John Doe",
        "file_path": "/media/ml_basics.pdf",
        "file_type": ".pdf",
        "file_size": 1048576,
        "upload_date": "2025-10-19T22:00:00Z",
        "metadata": {},
        "uploaded_by": 1,
        "uploaded_by_username": "john_doe",
        "chunk_count": 25
    }
]
```

---

### 3. Get Document Details

**Endpoint:** `GET /api/rag/documents/{id}/`

**Description:** Get detailed information about a specific document.

**Response:**
```json
{
    "id": 1,
    "title": "Machine Learning Basics",
    "author": "John Doe",
    "file_path": "/media/ml_basics.pdf",
    "file_type": ".pdf",
    "file_size": 1048576,
    "upload_date": "2025-10-19T22:00:00Z",
    "metadata": {
        "num_pages": 10,
        "created_at": "2025-10-19T22:00:00Z"
    },
    "uploaded_by": 1,
    "uploaded_by_username": "john_doe",
    "chunk_count": 25
}
```

---

### 4. Get Document Chunks

**Endpoint:** `GET /api/rag/documents/{id}/chunks/`

**Description:** Get all chunks from a specific document.

**Response:**
```json
[
    {
        "id": 1,
        "document": 1,
        "document_title": "Machine Learning Basics",
        "content": "Machine learning is a subset of artificial intelligence...",
        "chunk_index": 0,
        "metadata": {
            "title": "Machine Learning Basics",
            "author": "John Doe",
            "start_position": 0,
            "end_position": 1000
        },
        "created_at": "2025-10-19T22:00:00Z"
    }
]
```

---

### 5. Reindex Document

**Endpoint:** `POST /api/rag/documents/{id}/reindex/`

**Description:** Regenerate chunks and embeddings for a document.

**Response:**
```json
{
    "id": 1,
    "title": "Machine Learning Basics",
    "chunk_count": 25,
    "message": "Document reindexed successfully"
}
```

**Status Codes:**
- 200: Success
- 404: Document not found
- 500: Error during reindexing

---

### 6. Delete Document

**Endpoint:** `DELETE /api/rag/documents/{id}/`

**Description:** Delete a document and all its chunks.

**Status Codes:**
- 204: Successfully deleted
- 404: Document not found
- 500: Error during deletion

---

### 7. List Document Chunks

**Endpoint:** `GET /api/rag/chunks/`

**Description:** Get list of all document chunks across all documents.

**Response:**
```json
[
    {
        "id": 1,
        "document": 1,
        "document_title": "Machine Learning Basics",
        "content": "Machine learning is...",
        "chunk_index": 0,
        "metadata": {},
        "created_at": "2025-10-19T22:00:00Z"
    }
]
```

---

### 8. Get Chunk Details

**Endpoint:** `GET /api/rag/chunks/{id}/`

**Description:** Get details of a specific chunk.

---

### 9. List Query Logs

**Endpoint:** `GET /api/rag/query-logs/`

**Description:** Get list of all RAG query logs.

**Response:**
```json
[
    {
        "id": 1,
        "conversation_id": 1,
        "query": "What is machine learning?",
        "chunks_used": [
            {
                "id": 1,
                "document": 1,
                "document_title": "ML Basics",
                "content": "Machine learning is...",
                "chunk_index": 0
            }
        ],
        "response": "Machine learning is a subset of AI...",
        "timestamp": "2025-10-19T22:00:00Z",
        "execution_time": 1.234
    }
]
```

---

### 10. Get Query Log Details

**Endpoint:** `GET /api/rag/query-logs/{id}/`

**Description:** Get details of a specific query log including all chunks used.

---

## Error Responses

All error responses follow this format:

```json
{
    "error": "Error message description"
}
```

or for validation errors:

```json
{
    "field_name": [
        "Error message for this field"
    ]
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. Consider adding it for production:
- Use Django Rest Framework's throttling
- Configure in `settings.py` REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']

---

## Pagination

List endpoints support pagination using query parameters:
- `?page=2` - Get page 2
- `?page_size=20` - Set items per page

Example:
```
GET /api/rag/documents/?page=2&page_size=20
```

---

## Filtering & Searching

### Documents
- `?search=machine+learning` - Search in title and author
- `?file_type=.pdf` - Filter by file type

### Conversations
- `?search=AI` - Search in title

---

## Best Practices

1. **Always provide meaningful titles** when creating conversations
2. **Use instruction field** to provide context or specific requirements
3. **Adjust top_k** based on your needs (higher = more context, slower)
4. **Monitor query logs** to understand system performance
5. **Reindex documents** if you update chunking configuration

---

## Integration Examples

### React/Next.js Example

```javascript
// api/chatbot.js
export async function sendMessage(message, conversationId = null) {
  const response = await fetch('http://localhost:8000/api/chatbot/chat/send_message/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
      top_k: 5
    })
  });
  return response.json();
}

export async function uploadDocument(file, title, author) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('title', title);
  formData.append('author', author);
  
  const response = await fetch('http://localhost:8000/api/rag/documents/upload/', {
    method: 'POST',
    body: formData
  });
  return response.json();
}
```

### Python SDK Example

```python
import requests

class RAGChatbotClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def send_message(self, message, conversation_id=None, instruction="", top_k=5):
        url = f"{self.base_url}/api/chatbot/chat/send_message/"
        data = {
            "message": message,
            "conversation_id": conversation_id,
            "instruction": instruction,
            "top_k": top_k
        }
        response = requests.post(url, json=data)
        return response.json()
    
    def upload_document(self, file_path, title="", author=""):
        url = f"{self.base_url}/api/rag/documents/upload/"
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'title': title, 'author': author}
            response = requests.post(url, files=files, data=data)
        return response.json()
    
    def list_conversations(self):
        url = f"{self.base_url}/api/chatbot/conversations/"
        response = requests.get(url)
        return response.json()
```

---

## WebSocket Support (Future)

For real-time chat, consider implementing Django Channels:
```python
# Future feature
ws://localhost:8000/ws/chat/{conversation_id}/
```

---

**For more information, see the main README.md file.**
