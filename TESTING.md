# Testing Guide

## Running Tests

### Option 1: Run the basic test script
```bash
PYTHONPATH=/Users/vishaltathe/Antigravity/AILegacy python3 tests/test_cli.py
```

### Option 2: Run with virtual environment (recommended)
```bash
# Activate your virtual environment first
source venv/bin/activate

# Then run the test
PYTHONPATH=. python3 tests/test_cli.py
```

### Option 3: Install and use pytest (professional approach)
```bash
# Install pytest
pip install pytest

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_cli.py

# Run with verbose output
pytest -v tests/
```

## Important Notes

⚠️ **Before running tests:**
1. Make sure Ollama is installed and running (`ollama run llama3`)
2. Or modify the test to use a mock/stub instead of real LLM calls

## Current Test Status

The `tests/test_cli.py` file tests the RAG agent with sample documents. It will:
1. Create an in-memory database
2. Insert two test documents
3. Ask a question: "How to migrate the database?"
4. Print the answer from the RAG agent

**Note:** This test requires Ollama to be running to work properly.

## Creating Mock Tests (No Ollama Required)

If you want to test without Ollama, you can create unit tests that mock the LLM responses.
