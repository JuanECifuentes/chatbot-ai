# Setup Checklist

Use this checklist to ensure your RAG Chatbot is properly configured and ready to use.

## ☑️ Prerequisites

- [ ] Python 3.8 or higher installed
- [ ] PostgreSQL 12 or higher installed
- [ ] PostgreSQL server is running
- [ ] pgvector extension available (or compiled)
- [ ] Google Gemini API account created
- [ ] Gemini API key obtained

## ☑️ Database Setup

- [ ] PostgreSQL database created (rag_chatbot_db)
- [ ] Database user created with proper permissions
- [ ] Database connection tested (psql or pgAdmin)
- [ ] Database credentials recorded

## ☑️ Project Installation

- [ ] Project files downloaded/cloned
- [ ] Virtual environment created (`python -m venv venv`)
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] No installation errors reported

## ☑️ Configuration

- [ ] `.env` file created (copied from `.env.example`)
- [ ] Database credentials added to `.env`
  - [ ] DB_NAME set
  - [ ] DB_USER set
  - [ ] DB_PASSWORD set
  - [ ] DB_HOST set (usually localhost)
  - [ ] DB_PORT set (usually 5432)
- [ ] Gemini API key added to `.env`
  - [ ] GEMINI_API_KEY set (not default value)
- [ ] LLM model configured (default: gemini-2.0-flash-exp)
- [ ] Embedding model configured (default: models/text-embedding-004)
- [ ] RAG parameters reviewed and adjusted if needed
  - [ ] CHUNK_SIZE (default: 1000)
  - [ ] CHUNK_OVERLAP (default: 200)
  - [ ] TOP_K_RESULTS (default: 5)
  - [ ] MAX_CONTEXT_TOKENS (default: 4000)
  - [ ] EMBEDDING_DIMENSION (default: 768)

## ☑️ Django Setup

- [ ] Migrations created (`python manage.py makemigrations`)
- [ ] Migrations applied (`python manage.py migrate`)
- [ ] No migration errors
- [ ] pgvector extension initialized (`python manage.py init_pgvector`)
- [ ] Superuser created (`python manage.py createsuperuser`)
  - [ ] Username recorded
  - [ ] Password recorded
- [ ] Static files collected (if deploying)

## ☑️ Testing

- [ ] Installation test run (`python test_installation.py`)
- [ ] All tests passed
- [ ] Development server starts (`python manage.py runserver`)
- [ ] Server accessible at http://localhost:8000
- [ ] Admin interface accessible at http://localhost:8000/admin/
- [ ] Admin login successful

## ☑️ First Document Upload

- [ ] Test document prepared (PDF or DOCX)
- [ ] Document uploaded via API or admin
- [ ] Document processing completed
- [ ] Chunks created in database
- [ ] No errors during upload

## ☑️ First Chat Test

- [ ] Test query sent via API
- [ ] Response received successfully
- [ ] Response uses document context
- [ ] Conversation created
- [ ] Messages recorded in database

## ☑️ API Testing

- [ ] Chat endpoint tested (`POST /api/chatbot/chat/send_message/`)
- [ ] Document upload tested (`POST /api/rag/documents/upload/`)
- [ ] Conversation list tested (`GET /api/chatbot/conversations/`)
- [ ] Document list tested (`GET /api/rag/documents/`)
- [ ] All endpoints return expected responses
- [ ] No 500 errors

## ☑️ Admin Interface

- [ ] Users manageable
- [ ] Conversations viewable
- [ ] Messages inspectable
- [ ] Documents manageable
- [ ] Chunks viewable
- [ ] Query logs accessible

## ☑️ Documentation Review

- [ ] README.md read
- [ ] API_DOCUMENTATION.md reviewed
- [ ] QUICK_START.md followed
- [ ] PROJECT_SUMMARY.md understood
- [ ] API endpoints documented

## ☑️ Optional Production Setup

- [ ] DEBUG set to False
- [ ] SECRET_KEY changed to secure value
- [ ] ALLOWED_HOSTS configured
- [ ] CORS_ALLOWED_ORIGINS configured for frontend
- [ ] Static files configured
- [ ] Media files directory secured
- [ ] Database backups configured
- [ ] Logging configured
- [ ] Error monitoring set up
- [ ] Rate limiting added
- [ ] Authentication implemented
- [ ] HTTPS configured
- [ ] Firewall rules set

## ☑️ Security Review

- [ ] .env file in .gitignore
- [ ] No secrets committed to git
- [ ] Database password is strong
- [ ] Secret key is random and secure
- [ ] API key secured
- [ ] File upload size limits set
- [ ] CORS properly configured
- [ ] SQL injection protection verified (Django ORM)

## ☑️ Performance Optimization

- [ ] Database indexes reviewed
- [ ] Vector search tested with multiple documents
- [ ] Query response time acceptable
- [ ] Chunk size optimized for use case
- [ ] Context window sized appropriately
- [ ] PostgreSQL performance tuned (if needed)

## ☑️ Backup & Recovery

- [ ] Database backup procedure established
- [ ] Media files backup configured
- [ ] Recovery procedure tested
- [ ] Backup schedule set

## 🎯 Ready to Use!

Once all items are checked:

✅ Your RAG Chatbot is fully configured and operational!

### Quick Reference Commands

```bash
# Start server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Initialize pgvector
python manage.py init_pgvector

# Test installation
python test_installation.py

# Collect static files (production)
python manage.py collectstatic
```

### Troubleshooting

If something isn't working:

1. **Check the test script**: `python test_installation.py`
2. **Review logs**: Check console output for errors
3. **Verify .env**: Ensure all values are correct
4. **Check database**: Ensure PostgreSQL is running
5. **Review documentation**: See README.md and API_DOCUMENTATION.md

### Getting Help

- 📖 Read README.md for detailed information
- 🚀 Follow QUICK_START.md for step-by-step guide
- 📡 Check API_DOCUMENTATION.md for API details
- 🏗️ See PROJECT_SUMMARY.md for architecture overview

---

**Need support?** Create an issue in the repository with:
- Error message
- Steps to reproduce
- Your environment (OS, Python version, PostgreSQL version)
- Relevant configuration (without secrets!)
