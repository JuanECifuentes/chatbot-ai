#!/bin/bash

echo "==================================="
echo "RAG Chatbot Setup Script"
echo "==================================="
echo ""

echo "[1/6] Checking Python installation..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi
echo ""

echo "[2/6] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi
echo ""

echo "[3/6] Activating virtual environment..."
source venv/bin/activate
echo ""

echo "[4/6] Installing dependencies..."
pip install -r requirements.txt --quiet
echo "Dependencies installed"
echo ""

echo "[5/6] Checking for .env file..."
if [ ! -f ".env" ]; then
    echo ".env file not found. Copying from .env.example..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Please edit .env file and add your configuration:"
    echo "- Database credentials"
    echo "- Gemini API key"
    echo ""
    read -p "Press enter to continue..."
else
    echo ".env file found"
fi
echo ""

echo "[6/6] Running migrations..."
python manage.py makemigrations
python manage.py migrate
echo ""

echo "Setting up pgvector extension..."
python manage.py init_pgvector
echo ""

echo "==================================="
echo "Setup completed successfully!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Create a superuser: python manage.py createsuperuser"
echo "3. Run the server: python manage.py runserver"
echo ""
echo "Admin interface: http://localhost:8000/admin/"
echo "API documentation: See API_DOCUMENTATION.md"
echo ""
