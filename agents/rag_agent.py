"""RAG agent that uses Ollama (via OpenAI client) to generate answers based on retrieved documents.

Function provided:
- simple_rag_answer(query, docs) -> {answer, sources, confidence}

`docs` should be a list of dicts each containing at least 'filename' and 'content'.
"""
import re
import os
from collections import Counter
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure OpenAI client for Ollama
base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
api_key = "ollama" # required but unused by Ollama

client = OpenAI(base_url=base_url, api_key=api_key)

def _tokenize(text):
    return re.findall(r"\w+", text.lower())


def simple_rag_answer(query, docs=None):
    qtokens = _tokenize(query)
    if not docs:
        return {"answer": "I have no context documents. Upload docs to get better answers.", "sources": [], "confidence": 0.0}

    scores = []
    for d in docs:
        content = d.get("content", "")
        tokens = _tokenize(content)
        # simple score: number of shared tokens
        common = sum((Counter(tokens) & Counter(qtokens)).values())
        scores.append((common, d))

    scores.sort(reverse=True, key=lambda x: x[0])
    top = [s for s in scores if s[0] > 0][:3]
    
    if not top:
        return {"answer": "I couldn't find relevant content in your documents. Consider uploading architecture docs, db schemas, or runbooks.", "sources": [], "confidence": 0.2}

    # Build context from top docs
    context_snippets = []
    srcs = []
    for score, d in top:
        content = d.get("content", "")
        # Take a larger chunk for context, e.g., first 1000 chars or around keywords
        # For simplicity, we'll take the first 1000 characters of the doc if it's a match
        # In a real system, we'd use vector search to find the best chunk.
        snippet = content[:1000] + "..." if len(content) > 1000 else content
        context_snippets.append(f"Document: {d.get('filename')}\nContent: {snippet}")
        srcs.append(d.get('filename'))

    context_text = "\n\n".join(context_snippets)
    
    system_prompt = """You are a helpful assistant for legacy system modernization. 
    Answer the user's question based ONLY on the provided context documents. 
    If the answer is not in the context, say you don't know.
    Cite the document filenames when possible."""

    user_prompt = f"""Context:
    {context_text}

    Question: {query}
    """

    try:
        response = client.chat.completions.create(
            model=os.getenv("OLLAMA_MODEL", "llama3"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        answer = response.choices[0].message.content
        confidence = 0.9 # High confidence if we got a response
    except Exception as e:
        answer = f"Error generating answer: {str(e)}"
        confidence = 0.0

    return {"answer": answer, "sources": srcs, "confidence": confidence}