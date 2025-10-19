# Quick Start Guide

## 1. Initial Setup (5 minutes)

### Step 1: Install PostgreSQL
- Download from: https://www.postgresql.org/download/
- Create a database named `rag_chatbot_db`

### Step 2: Get Gemini API Key
- Go to: https://ai.google.dev/
- Create an account and get your API key

### Step 3: Configure Environment
```bash
# Copy the example environment file
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# Edit .env and add:
# - Your database password
# - Your Gemini API key
```

### Step 4: Run Setup
```bash
# Windows
setup.bat

# Linux/Mac
chmod +x setup.sh
./setup.sh
```

### Step 5: Create Admin User
```bash
python manage.py createsuperuser
```

### Step 6: Start Server
```bash
python manage.py runserver
```

🎉 Server is now running at http://localhost:8000

---

## 2. Upload Your First Document (2 minutes)

### Using cURL:
```bash
curl -X POST http://localhost:8000/api/rag/documents/upload/ \
  -F "file=@your_document.pdf" \
  -F "title=My First Document" \
  -F "author=Your Name"
```

### Using Python:
```python
import requests

url = "http://localhost:8000/api/rag/documents/upload/"
with open("your_document.pdf", "rb") as f:
    files = {"file": f}
    data = {"title": "My First Document", "author": "Your Name"}
    response = requests.post(url, files=files, data=data)
    print(response.json())
```

### Using Postman:
1. Create a new POST request
2. URL: `http://localhost:8000/api/rag/documents/upload/`
3. Body → form-data
4. Add key "file" (type: File) and select your PDF/DOCX
5. Add key "title" (type: Text) with your document title
6. Send

---

## 3. Chat with Your Documents (1 minute)

### Using cURL:
```bash
curl -X POST http://localhost:8000/api/chatbot/chat/send_message/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is this document about?",
    "top_k": 5
  }'
```

### Using Python:
```python
import requests

url = "http://localhost:8000/api/chatbot/chat/send_message/"
data = {
    "message": "What is this document about?",
    "top_k": 5
}
response = requests.post(url, json=data)
print(response.json()["response"]["content"])
```

### Using JavaScript/Fetch:
```javascript
const response = await fetch('http://localhost:8000/api/chatbot/chat/send_message/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        message: 'What is this document about?',
        top_k: 5
    })
});

const data = await response.json();
console.log(data.response.content);
```

---

## 4. Common Tasks

### View All Documents
```bash
curl http://localhost:8000/api/rag/documents/
```

### View All Conversations
```bash
curl http://localhost:8000/api/chatbot/conversations/
```

### Continue a Conversation
```python
# Get conversation_id from previous response
data = {
    "conversation_id": 1,  # Use existing conversation
    "message": "Tell me more about that"
}
```

### Delete a Document
```bash
curl -X DELETE http://localhost:8000/api/rag/documents/1/
```

### View Query Logs (for debugging)
```bash
curl http://localhost:8000/api/rag/query-logs/
```

---

## 5. Access Admin Panel

1. Go to: http://localhost:8000/admin/
2. Login with your superuser credentials
3. You can now:
   - View all users, conversations, and messages
   - Manage documents and chunks
   - Inspect query logs
   - View embeddings statistics

---

## 6. Customize RAG Parameters

Edit your `.env` file:

```env
# Smaller chunks for more precise retrieval
CHUNK_SIZE=500
CHUNK_OVERLAP=100

# Retrieve more context
TOP_K_RESULTS=10

# Allow more context tokens
MAX_CONTEXT_TOKENS=8000
```

Then reindex your documents:
```bash
curl -X POST http://localhost:8000/api/rag/documents/1/reindex/
```

---

## 7. Frontend Integration

### Basic React Component
```jsx
import { useState } from 'react';

function ChatInterface() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    setLoading(true);
    const res = await fetch('http://localhost:8000/api/chatbot/chat/send_message/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    const data = await res.json();
    setResponse(data.response.content);
    setLoading(false);
  };

  return (
    <div>
      <input 
        value={message} 
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask a question..."
      />
      <button onClick={sendMessage} disabled={loading}>
        {loading ? 'Thinking...' : 'Send'}
      </button>
      {response && <div><strong>Response:</strong> {response}</div>}
    </div>
  );
}
```

---

## 8. Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
# Windows: Check Services
# Linux: sudo systemctl status postgresql
```

### pgvector Extension Error
```bash
python manage.py init_pgvector
```

### Gemini API Error
- Verify your API key in .env
- Check API quota at https://ai.google.dev/

### Document Upload Fails
- Check file size (adjust Django settings if needed)
- Ensure media directory exists and is writable
- Verify file format is PDF or DOCX

### No Context in Responses
- Check if documents are uploaded
- Verify embeddings are generated
- Try increasing TOP_K_RESULTS

---

## 9. Performance Optimization

### For Production:
1. Set `DEBUG=False` in .env
2. Configure proper `ALLOWED_HOSTS`
3. Use PostgreSQL connection pooling
4. Add caching for embeddings
5. Implement rate limiting
6. Set up proper CORS policies
7. Use CDN for static files

### Database Optimization:
```sql
-- Create indexes for better performance
CREATE INDEX idx_chunks_document ON document_chunks(document_id);
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_conversations_user ON conversations(user_id);
```

---

## 10. Next Steps

1. **Build a Frontend**: Use React, Vue, or Next.js
2. **Add Authentication**: Implement JWT or OAuth
3. **Deploy**: Use Docker, AWS, or Heroku
4. **Monitor**: Set up logging and analytics
5. **Scale**: Add load balancing and caching

---

## Need Help?

- 📖 See full README.md for detailed documentation
- 📡 Check API_DOCUMENTATION.md for API reference
- 🐛 Report issues on GitHub
- 💬 Join our community discussions

---

**Happy Coding! 🚀**
