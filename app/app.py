"""Streamlit frontend (minimal) with CLI fallback.

Run (preferred):
  streamlit run app/app.py

Fallback:
  python app/app.py

This app depends on the local modules: database.connector and agents.rag_agent
"""
from datetime import datetime
import os
import sys

# Add project root to sys.path so we can import from database/ and agents/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Try optional import
try:
    import streamlit as st
    STREAMLIT = True
except Exception:
    STREAMLIT = False

# local imports
from database.connector import get_db
from agents.rag_agent import simple_rag_answer

DB = get_db()


def run_streamlit():
    st.set_page_config(page_title="Legacy Modernization Advisor", layout="wide")
    st.title("Legacy Modernization Advisor — MVP")

    st.sidebar.header("Upload (text files)")
    uploaded = st.sidebar.file_uploader("Upload .txt files", accept_multiple_files=True, type=["txt"])
    if uploaded:
        for f in uploaded:
            raw = f.read().decode(errors='ignore')
            doc = {"filename": f.name, "content": raw, "uploaded_at": datetime.utcnow().isoformat()}
            DB.insert_document(doc)
        st.sidebar.success(f"Uploaded {len(uploaded)} file(s)")

    st.subheader("Chat")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m.get("role", "user")):
            st.write(m.get("content"))

    q = st.chat_input("Ask about modernization...")
    if q:
        st.session_state.messages.append({"role": "user", "content": q, "ts": datetime.utcnow().isoformat()})
        
        # Show loading state while processing
        with st.spinner('Processing your question...'):
            docs = DB.list_documents()
            resp = simple_rag_answer(q, docs)
            st.session_state.messages.append({"role": "assistant", "content": resp["answer"], "ts": datetime.utcnow().isoformat()})
        
        with st.chat_message("assistant"):
            st.write(resp["answer"])
        # persist conversation
        DB.insert_conversation({"timestamp": datetime.utcnow().isoformat(), "messages": st.session_state.messages})
        st.rerun()




def run_cli():
    print("Streamlit not available. Running simple CLI.")
    print("Commands:\n  upload <dir>\n  docs\n  ask <question>\n  exit")
    while True:
        try:
            cmd = input("cmd> ").strip()
        except Exception:
            print("Interactive input not available. Exiting.")
            break
        if not cmd:
            continue
        if cmd in ("exit", "quit"):
            break
        if cmd.startswith("upload "):
            path = cmd[len("upload "):].strip()
            if not os.path.isdir(path):
                print("Invalid path")
                continue
            count = 0
            for fn in os.listdir(path):
                if not fn.lower().endswith(".txt"):
                    continue
                with open(os.path.join(path, fn), "r", errors="ignore") as fh:
                    content = fh.read()
                DB.insert_document({"filename": fn, "content": content, "uploaded_at": datetime.utcnow().isoformat()})
                count += 1
            print(f"Uploaded {count} files")
            continue
        if cmd == "docs":
            docs = DB.list_documents()
            for i, d in enumerate(docs, 1):
                print(i, d.get("filename"))
            continue
        if cmd.startswith("ask "):
            q = cmd[len("ask "):].strip()
            docs = DB.list_documents()
            resp = simple_rag_answer(q, docs)
            print("\n---Answer---\n")
            print(resp["answer"])
            print("Sources:", resp.get("sources"))
            DB.insert_conversation({"timestamp": datetime.utcnow().isoformat(), "messages": [{"role": "user", "content": q}, {"role": "assistant", "content": resp["answer"]}]})
            continue
        print("Unknown command")


if __name__ == '__main__':
    if STREAMLIT:
        run_streamlit()
    else:
        run_cli()
