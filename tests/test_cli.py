"""Basic test harness for run_cli_commands-like behavior using agents and in-memory DB.
This is not a pytest module but a tiny script you can run to validate flows.
"""
from database.connector import InMemoryDB
from agents.rag_agent import simple_rag_answer


def test_end_to_end():
    db = InMemoryDB()
    # simulate upload
    db.insert_document({"filename": "a.txt", "content": "This legacy app uses Oracle DB and Tomcat.", "uploaded_at": "now"})
    db.insert_document({"filename": "b.txt", "content": "We are considering Dockerizing the app and moving to microservices.", "uploaded_at": "now"})

    docs = db.list_documents()
    resp = simple_rag_answer("How to migrate the database?", docs)
    print("Answer:", resp)


if __name__ == '__main__':
    test_end_to_end()