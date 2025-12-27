#!/bin/bash

# EduGenius Startup Script

echo "=================================================="
echo "🎓 EduGenius - AI-Powered Educational Assistant"
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  WARNING: .env file not found!"
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo ""
    echo "📝 Please edit .env file and add your API keys before running the application."
    echo "   At minimum, you need to configure one LLM provider:"
    echo "   - DEEPSEEK_API_KEY (recommended)"
    echo "   - OPENAI_API_KEY"
    echo "   - ANTHROPIC_API_KEY"
    echo ""
    read -p "Press Enter to continue or CTRL+C to exit and configure .env..."
fi

# Run the application
echo ""
echo "Starting EduGenius server..."
python3 run.py
