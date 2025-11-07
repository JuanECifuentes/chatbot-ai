# Quick Start Guide - Using the New Chat Interface

## 🚀 Getting Started

### Step 1: Start the Server
```bash
# Activate virtual environment (if not already activated)
.\venv\Scripts\Activate.ps1  # Windows
# or
source venv/bin/activate  # Linux/Mac

# Start Django server
python manage.py runserver
```

### Step 2: Open the Interface
Open your web browser and navigate to:
```
http://localhost:8000/
```

You should see a dark-themed chat interface similar to ChatGPT!

---

## 📝 Using the Interface

### Starting Your First Conversation

1. **Upload Documents First** (if you haven't already)
   - Use the API or admin panel to upload PDF/DOCX files
   - Documents need to be indexed before the chatbot can use them
   
   Example using cURL:
   ```bash
   curl -X POST http://localhost:8000/api/rag/documents/upload/ \
     -F "file=@your_document.pdf" \
     -F "title=My Document"
   ```

2. **Type Your Question**
   - Click on the text box at the bottom
   - Type your question
   - Press `Enter` or click the send button

3. **Get Response**
   - The bot will show a loading animation (three dots)
   - Response appears based ONLY on your uploaded documents
   - If the answer isn't in the documents, the bot will tell you

### Managing Conversations

#### Create New Chat
- Click the **"New Chat"** button in the sidebar
- This starts a fresh conversation
- Previous chats are saved automatically

#### Resume Previous Chat
- Look at the **conversation history** in the sidebar
- Click any conversation to continue it
- The active conversation is highlighted

#### Switch Between Chats
- Simply click different conversations in the sidebar
- All message history is preserved
- No data is lost when switching

---

## 💡 Tips & Tricks

### Keyboard Shortcuts
- `Enter` → Send message
- `Shift + Enter` → New line in message
- Type and press Enter for quick questions

### Message Formatting
The interface supports basic formatting:
- `**bold text**` → **bold text**
- `*italic text*` → *italic text*
- `` `code` `` → `code`

### Best Practices
1. **Upload relevant documents first** - The bot can only answer based on uploaded content
2. **Be specific** - Clear questions get better answers
3. **Check conversation history** - Review previous chats in the sidebar
4. **Start new chats** - Separate topics for better organization

---

## 🎯 Example Usage Scenarios

### Scenario 1: Technical Documentation Query
```
You: How do I configure the database connection?
Bot: [Provides answer from your technical documentation]
```

### Scenario 2: Knowledge Base Question
```
You: What is the refund policy?
Bot: [Provides answer from your policy documents]
```

### Scenario 3: No Information Available
```
You: What is the capital of France?
Bot: I don't have enough information in my knowledge base to answer 
     this question. Please upload relevant documents or rephrase your question.
```
*(Because this info isn't in your uploaded documents)*

---

## 🔧 Testing the RAG Restriction

To verify the bot ONLY uses uploaded documents:

1. **Test WITH document content:**
   ```
   Upload: A document about Python programming
   Ask: "What is Python used for?"
   Expected: Detailed answer from the document
   ```

2. **Test WITHOUT document content:**
   ```
   No documents uploaded about history
   Ask: "Who was the first president of the USA?"
   Expected: "I don't have enough information..."
   ```

This confirms the LLM is restricted to RAG knowledge only! ✅

---

## 🐛 Troubleshooting

### Issue: "I don't have enough information" for everything

**Solution:**
1. Upload documents via API:
   ```bash
   curl -X POST http://localhost:8000/api/rag/documents/upload/ \
     -F "file=@document.pdf"
   ```
2. Verify documents exist:
   ```
   http://localhost:8000/api/rag/documents/
   ```
3. Check chunks were created:
   ```
   http://localhost:8000/api/rag/chunks/
   ```

### Issue: Messages not sending

**Solution:**
1. Check browser console (F12) for errors
2. Verify server is running: `python manage.py runserver`
3. Try refreshing the page (Ctrl+F5)
4. Check network tab in DevTools

### Issue: Conversations not loading

**Solution:**
1. Ensure database is running (PostgreSQL)
2. Check for migrations: `python manage.py migrate`
3. Verify API works: Visit `http://localhost:8000/api/chatbot/conversations/`

---

## 📱 Mobile Usage

The interface is responsive and works on mobile devices:
- Sidebar adapts to smaller screens
- Touch-friendly buttons
- Optimized message display
- Smooth scrolling

---

## 🔐 Security Note

Currently, the interface doesn't require login. For production:
1. Add user authentication
2. Implement proper authorization
3. Add rate limiting
4. Use HTTPS

---

## 🎨 Interface Features

### Visual Indicators
- 💬 User messages: Dark gray background
- 🤖 Bot messages: Darker gray background
- ⏳ Loading: Animated three dots
- ✓ Active chat: Highlighted in sidebar
- 🕐 Timestamps: Relative time display

### Animations
- Smooth message appearance
- Loading dots animation
- Hover effects on buttons
- Scroll animations

---

## 📊 What the Bot Can Do

✅ **Answer questions** from uploaded documents  
✅ **Maintain context** within a conversation  
✅ **Handle follow-up questions**  
✅ **Provide accurate information** from RAG  
✅ **Admit when it doesn't know** something  

❌ **Cannot use general knowledge** (by design)  
❌ **Cannot answer without documents** (feature, not bug)  
❌ **Cannot access the internet**  
❌ **Cannot remember across different conversations** (each is isolated)  

---

## 🚦 System Status Check

### Quick Health Check
Visit these URLs to verify everything works:

1. **API Health:**
   ```
   http://localhost:8000/api/chatbot/conversations/
   ```
   Should return JSON with conversation list

2. **Documents:**
   ```
   http://localhost:8000/api/rag/documents/
   ```
   Should show your uploaded documents

3. **Chat Interface:**
   ```
   http://localhost:8000/
   ```
   Should load the chat UI

All three should work! ✅

---

## 📚 Additional Resources

- **Full API Documentation:** See `API_DOCUMENTATION.md`
- **Implementation Details:** See `IMPLEMENTATION_GUIDE.md`
- **Project Overview:** See `PROJECT_SUMMARY.md`
- **Architecture:** See `ARCHITECTURE.md`

---

## 🎉 You're Ready!

The chatbot is now ready to use with:
1. ✅ Strict RAG-only responses
2. ✅ Beautiful web interface
3. ✅ Conversation management
4. ✅ Real-time messaging

Start chatting at: **http://localhost:8000/**

Enjoy your intelligent document-based chatbot! 🚀
