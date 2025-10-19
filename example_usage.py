"""
Example usage script for RAG Chatbot API

This script demonstrates how to interact with the RAG Chatbot API.
Run this after the server is up and running.

Usage: python example_usage.py
"""

import requests
import json
import time
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
API_CHATBOT = f"{BASE_URL}/api/chatbot"
API_RAG = f"{BASE_URL}/api/rag"


class RAGChatbotClient:
    """Simple client for RAG Chatbot API"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.chatbot_url = f"{base_url}/api/chatbot"
        self.rag_url = f"{base_url}/api/rag"
    
    def upload_document(self, file_path, title="", author="", metadata=None):
        """Upload a document to the RAG system"""
        url = f"{self.rag_url}/documents/upload/"
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'title': title or Path(file_path).stem,
                'author': author or 'Unknown'
            }
            if metadata:
                data['metadata'] = json.dumps(metadata)
            
            response = requests.post(url, files=files, data=data)
            return response.json()
    
    def list_documents(self):
        """List all uploaded documents"""
        url = f"{self.rag_url}/documents/"
        response = requests.get(url)
        return response.json()
    
    def get_document(self, document_id):
        """Get details of a specific document"""
        url = f"{self.rag_url}/documents/{document_id}/"
        response = requests.get(url)
        return response.json()
    
    def send_message(self, message, conversation_id=None, instruction="", top_k=5):
        """Send a message to the chatbot"""
        url = f"{self.chatbot_url}/chat/send_message/"
        data = {
            'message': message,
            'top_k': top_k
        }
        
        if conversation_id:
            data['conversation_id'] = conversation_id
        if instruction:
            data['instruction'] = instruction
        
        response = requests.post(url, json=data)
        return response.json()
    
    def list_conversations(self):
        """List all conversations"""
        url = f"{self.chatbot_url}/conversations/"
        response = requests.get(url)
        return response.json()
    
    def get_conversation(self, conversation_id):
        """Get details of a specific conversation"""
        url = f"{self.chatbot_url}/conversations/{conversation_id}/"
        response = requests.get(url)
        return response.json()
    
    def get_query_logs(self):
        """Get query logs"""
        url = f"{self.rag_url}/query-logs/"
        response = requests.get(url)
        return response.json()


def print_separator(title=""):
    """Print a nice separator"""
    if title:
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}\n")
    else:
        print(f"\n{'-' * 60}\n")


def example_1_upload_document(client):
    """Example: Upload a document"""
    print_separator("Example 1: Upload Document")
    
    # Note: Replace with an actual file path
    file_path = "sample_document.pdf"
    
    print(f"Attempting to upload: {file_path}")
    
    try:
        result = client.upload_document(
            file_path=file_path,
            title="Sample Document",
            author="John Doe",
            metadata={"category": "tutorial", "language": "en"}
        )
        
        print("✓ Document uploaded successfully!")
        print(f"  Document ID: {result.get('id')}")
        print(f"  Title: {result.get('title')}")
        print(f"  Chunks created: {result.get('chunk_count')}")
        
        return result.get('id')
    
    except FileNotFoundError:
        print(f"✗ File not found: {file_path}")
        print("  Please create a sample document or update the file path")
        return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def example_2_list_documents(client):
    """Example: List all documents"""
    print_separator("Example 2: List Documents")
    
    try:
        documents = client.list_documents()
        
        if documents:
            print(f"Found {len(documents)} document(s):")
            for doc in documents:
                print(f"\n  ID: {doc['id']}")
                print(f"  Title: {doc['title']}")
                print(f"  Author: {doc['author']}")
                print(f"  Type: {doc['file_type']}")
                print(f"  Chunks: {doc['chunk_count']}")
        else:
            print("No documents found. Upload some documents first!")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def example_3_chat_simple(client):
    """Example: Simple chat without conversation history"""
    print_separator("Example 3: Simple Chat")
    
    question = "What is machine learning?"
    
    print(f"Asking: {question}")
    
    try:
        result = client.send_message(
            message=question,
            top_k=3
        )
        
        print(f"\n✓ Response received:")
        print(f"  Conversation ID: {result['conversation_id']}")
        print(f"  Chunks used: {result['chunks_used']}")
        print(f"  Execution time: {result['execution_time']:.2f}s")
        print(f"\n  Assistant: {result['response']['content']}")
        
        return result['conversation_id']
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def example_4_chat_with_context(client, conversation_id):
    """Example: Continue conversation with context"""
    print_separator("Example 4: Chat with Context")
    
    if not conversation_id:
        print("No conversation ID provided. Starting new conversation...")
        conversation_id = None
    
    question = "Can you explain that in simpler terms?"
    
    print(f"Continuing conversation {conversation_id}")
    print(f"Asking: {question}")
    
    try:
        result = client.send_message(
            message=question,
            conversation_id=conversation_id,
            instruction="Explain in simple terms suitable for beginners"
        )
        
        print(f"\n✓ Response received:")
        print(f"  Assistant: {result['response']['content']}")
        
        return result['conversation_id']
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def example_5_view_conversation(client, conversation_id):
    """Example: View full conversation"""
    print_separator("Example 5: View Conversation")
    
    if not conversation_id:
        print("No conversation ID provided.")
        return
    
    try:
        conversation = client.get_conversation(conversation_id)
        
        print(f"Conversation: {conversation['title'] or 'Untitled'}")
        print(f"Created: {conversation['created_at']}")
        print(f"Messages: {len(conversation['messages'])}")
        
        print("\nFull conversation:")
        for msg in conversation['messages']:
            sender = "You" if msg['sender'] == 'user' else "Assistant"
            print(f"\n  {sender}: {msg['content']}")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def example_6_query_logs(client):
    """Example: View query logs"""
    print_separator("Example 6: Query Logs")
    
    try:
        logs = client.get_query_logs()
        
        if logs:
            print(f"Found {len(logs)} query log(s):")
            for log in logs[:3]:  # Show first 3
                print(f"\n  Query: {log['query'][:100]}...")
                print(f"  Chunks used: {len(log['chunks_used'])}")
                print(f"  Execution time: {log['execution_time']:.2f}s")
        else:
            print("No query logs found.")
    
    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    """Main example script"""
    print_separator("RAG Chatbot API - Usage Examples")
    
    # Initialize client
    client = RAGChatbotClient(BASE_URL)
    
    # Check if server is running
    try:
        response = requests.get(BASE_URL)
        print("✓ Server is running!")
    except requests.exceptions.ConnectionError:
        print("✗ Error: Cannot connect to server")
        print(f"  Make sure the server is running at {BASE_URL}")
        print("  Run: python manage.py runserver")
        return
    
    # Run examples
    print("\nNote: Some examples may fail if no documents are uploaded.")
    print("Upload a document first using Example 1 or the admin interface.")
    
    input("\nPress Enter to continue...")
    
    # Example 1: Upload document (optional, will fail if file doesn't exist)
    document_id = example_1_upload_document(client)
    time.sleep(1)
    
    # Example 2: List documents
    example_2_list_documents(client)
    time.sleep(1)
    
    # Example 3: Simple chat
    conversation_id = example_3_chat_simple(client)
    time.sleep(1)
    
    # Example 4: Continue conversation
    if conversation_id:
        conversation_id = example_4_chat_with_context(client, conversation_id)
        time.sleep(1)
    
    # Example 5: View full conversation
    if conversation_id:
        example_5_view_conversation(client, conversation_id)
        time.sleep(1)
    
    # Example 6: View query logs
    example_6_query_logs(client)
    
    print_separator("Examples Complete!")
    print("\nFor more information:")
    print("  - API Documentation: API_DOCUMENTATION.md")
    print("  - Quick Start Guide: QUICK_START.md")
    print("  - Admin Interface: http://localhost:8000/admin/")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
