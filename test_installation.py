"""
Test script to verify RAG Chatbot installation and basic functionality
Run with: python test_installation.py
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rag_chatbot.settings')
django.setup()

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    try:
        import rest_framework
        import psycopg2
        import google.generativeai as genai
        from pypdf import PdfReader
        from docx import Document
        from pgvector.django import VectorField
        print("✓ All required packages imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_database_connection():
    """Test database connection"""
    print("\nTesting database connection...")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✓ Connected to PostgreSQL: {version}")
        return True
    except Exception as e:
        print(f"✗ Database connection error: {e}")
        return False


def test_models():
    """Test if models are properly configured"""
    print("\nTesting models...")
    try:
        from chatbot.models import User, Conversation, Message
        from rag_engine.models import SourceDocument, DocumentChunk, RAGQueryLog
        print("✓ All models imported successfully")
        return True
    except Exception as e:
        print(f"✗ Model error: {e}")
        return False


def test_migrations():
    """Check if migrations are applied"""
    print("\nChecking migrations...")
    try:
        from django.db.migrations.executor import MigrationExecutor
        from django.db import connection
        
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        
        if plan:
            print(f"✗ Unapplied migrations found: {len(plan)}")
            print("  Run: python manage.py migrate")
            return False
        else:
            print("✓ All migrations applied")
            return True
    except Exception as e:
        print(f"✗ Migration check error: {e}")
        return False


def test_pgvector():
    """Test if pgvector extension is enabled"""
    print("\nTesting pgvector extension...")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
            result = cursor.fetchone()
            if result:
                print("✓ pgvector extension is enabled")
                return True
            else:
                print("✗ pgvector extension not found")
                print("  Run: python manage.py init_pgvector")
                return False
    except Exception as e:
        print(f"✗ pgvector test error: {e}")
        return False


def test_gemini_config():
    """Test Gemini API configuration"""
    print("\nTesting Gemini configuration...")
    try:
        from django.conf import settings
        
        if not settings.GEMINI_API_KEY:
            print("✗ GEMINI_API_KEY not set in environment")
            print("  Add your API key to .env file")
            return False
        
        if settings.GEMINI_API_KEY == "your_gemini_api_key_here":
            print("✗ GEMINI_API_KEY still has default value")
            print("  Update with your actual API key in .env file")
            return False
        
        print(f"✓ Gemini API key configured")
        print(f"  LLM Model: {settings.LLM_MODEL}")
        print(f"  Embedding Model: {settings.EMBEDDING_MODEL}")
        print(f"  Embedding Dimension: {settings.EMBEDDING_DIMENSION}")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False


def test_rag_config():
    """Test RAG configuration"""
    print("\nTesting RAG configuration...")
    try:
        from django.conf import settings
        
        print(f"  Chunk Size: {settings.CHUNK_SIZE}")
        print(f"  Chunk Overlap: {settings.CHUNK_OVERLAP}")
        print(f"  Top K Results: {settings.TOP_K_RESULTS}")
        print(f"  Max Context Tokens: {settings.MAX_CONTEXT_TOKENS}")
        print("✓ RAG configuration loaded")
        return True
    except Exception as e:
        print(f"✗ RAG configuration error: {e}")
        return False


def test_media_directory():
    """Test if media directory exists and is writable"""
    print("\nTesting media directory...")
    try:
        from django.conf import settings
        import os
        
        media_root = settings.MEDIA_ROOT
        
        if not os.path.exists(media_root):
            os.makedirs(media_root)
            print(f"✓ Created media directory: {media_root}")
        else:
            print(f"✓ Media directory exists: {media_root}")
        
        test_file = os.path.join(media_root, '.test_write')
        try:
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            print("✓ Media directory is writable")
            return True
        except:
            print("✗ Media directory is not writable")
            return False
    except Exception as e:
        print(f"✗ Media directory error: {e}")
        return False


def main():
    print("=" * 60)
    print("RAG Chatbot Installation Test")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_database_connection,
        test_models,
        test_migrations,
        test_pgvector,
        test_gemini_config,
        test_rag_config,
        test_media_directory,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 60)
    
    if all(results):
        print("\n✅ All tests passed! Your installation is ready.")
        print("\nNext steps:")
        print("1. Create a superuser: python manage.py createsuperuser")
        print("2. Start the server: python manage.py runserver")
        print("3. Upload a document and start chatting!")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("- Run migrations: python manage.py migrate")
        print("- Initialize pgvector: python manage.py init_pgvector")
        print("- Configure .env file with your settings")
    
    return all(results)


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
