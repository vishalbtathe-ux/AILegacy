#!/bin/bash

# AILegacy Setup Script for New System
# This script automates the setup process

set -e  # Exit on error

echo "🚀 Starting AILegacy setup..."

# Check if already in AILegacy directory
if [ ! -f "requirements.txt" ]; then
    echo "📦 Cloning repository..."
    git clone https://github.com/vishalbtathe-ux/AILegacy.git
    cd AILegacy
else
    echo "✅ Already in AILegacy directory"
fi

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cat > .env << EOF
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3.2:1b
EOF
    echo "✅ .env file created"
else
    echo "⚠️  .env file already exists, skipping..."
fi

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama not found. Please install from https://ollama.com"
    echo "   On Mac: brew install ollama"
else
    echo "✅ Ollama is installed"
    
    # Pull the model
    echo "📥 Pulling llama3.2:1b model..."
    ollama pull llama3.2:1b
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "To run the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Start Ollama (if not running): ollama serve"
echo "  3. Run the app: streamlit run app/app.py"
echo ""
echo "For testing: PYTHONPATH=. python3 tests/test_cli.py"
