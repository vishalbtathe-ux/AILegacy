# Performance Optimization Guide

## Current Optimizations Applied

### 1. Reduced Context Size
- Changed document snippet size from 1000 to 500 characters
- This reduces the amount of text sent to Ollama, speeding up processing

### 2. Limited Response Length
- Added `max_tokens=300` to limit response length
- Shorter responses = faster generation

### 3. Disabled Streaming
- Set `stream=False` for simpler processing

## Additional Ways to Speed Up

### Option 1: Use a Smaller/Faster Model
Instead of `llama3`, try a smaller model in your `.env`:
```bash
OLLAMA_MODEL=llama3.2:1b  # Much faster, smaller model
# or
OLLAMA_MODEL=phi3:mini    # Another fast option
```

### Option 2: Enable GPU Acceleration
If you have a Mac with Apple Silicon (M1/M2/M3):
- Ollama automatically uses Metal for GPU acceleration
- Make sure Ollama is updated to the latest version

### Option 3: Reduce Number of Documents
- Only upload the most relevant documents
- Keep document sizes smaller

### Option 4: Add Caching (Advanced)
- Cache frequently asked questions
- Store recent responses in session state

## Typical Response Times

With current setup:
- **First query**: 5-15 seconds (model loading)
- **Subsequent queries**: 3-8 seconds (model already loaded)

With smaller model (llama3.2:1b):
- **First query**: 2-5 seconds
- **Subsequent queries**: 1-3 seconds

## Try a Faster Model

Run this command to download a faster model:
```bash
ollama pull llama3.2:1b
```

Then update your `.env`:
```bash
OLLAMA_MODEL=llama3.2:1b
```
