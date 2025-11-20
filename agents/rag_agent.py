"""Very small RAG-style agent that does keyword matching over stored documents.
This is a placeholder for a true embedding+vectorstore+LLM pipeline.

Function provided:
- simple_rag_answer(query, docs) -> {answer, sources, confidence}

`docs` should be a list of dicts each containing at least 'filename' and 'content'.
"""
import re
from collections import Counter


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
        # fallback: return short general guidance
        return {"answer": "I couldn't find relevant content in your documents. Consider uploading architecture docs, db schemas, or runbooks.", "sources": [], "confidence": 0.2}

    # Build answer by quoting snippets from top docs
    snippets = []
    srcs = []
    for score, d in top:
        content = d.get("content", "")
        # find a sentence containing the first matching keyword
        for tk in qtokens:
            idx = content.lower().find(tk)
            if idx != -1:
                start = max(0, content.rfind('.', 0, idx) + 1)
                end = content.find('.', idx)
                if end == -1:
                    end = min(len(content), idx + 200)
                snippet = content[start:end].strip()
                if snippet:
                    snippets.append(f"From {d.get('filename')}: {snippet}")
                    break
        srcs.append(d.get('filename'))

    answer = "\n\n".join(snippets)
    confidence = min(0.9, 0.2 + 0.2 * len(top))
    return {"answer": answer, "sources": srcs, "confidence": confidence}