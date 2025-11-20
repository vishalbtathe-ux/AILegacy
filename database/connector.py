"""Simple MongoDB connector with in-memory fallback.

Provides: get_db() -> object with insert_document, insert_conversation, insert_feedback,
list_documents, list_conversations, list_feedback.
"""
import os
from datetime import datetime

try:
    from pymongo import MongoClient
    PYMONGO = True
except Exception:
    PYMONGO = False


class InMemoryDB:
    def __init__(self):
        self._docs = []
        self._convs = []
        self._fb = []

    def insert_document(self, doc):
        doc.setdefault("_id", len(self._docs) + 1)
        self._docs.append(doc)
        return doc

    def insert_conversation(self, conv):
        conv.setdefault("_id", len(self._convs) + 1)
        self._convs.append(conv)
        return conv

    def insert_feedback(self, fb):
        fb.setdefault("_id", len(self._fb) + 1)
        self._fb.append(fb)
        return fb

    def list_documents(self):
        return list(self._docs)

    def list_conversations(self):
        return list(self._convs)

    def list_feedback(self):
        return list(self._fb)


def get_db():
    """Return a DB wrapper. If MONGODB_URI is provided and pymongo is installed,
    try connecting. Otherwise return InMemoryDB.
    """
    uri = os.getenv("MONGODB_URI")
    if PYMONGO and uri:
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=3000)
            client.server_info()
            db = client[os.getenv("MONGODB_DB", "modernization_app")]
            docs = db["documents"]
            convs = db["conversations"]
            fbs = db["feedback"]

            class MongoWrapper:
                @staticmethod
                def insert_document(doc):
                    return docs.insert_one(doc)

                @staticmethod
                def insert_conversation(conv):
                    return convs.insert_one(conv)

                @staticmethod
                def insert_feedback(fb):
                    return fbs.insert_one(fb)

                @staticmethod
                def list_documents():
                    return list(docs.find())

                @staticmethod
                def list_conversations():
                    return list(convs.find())

                @staticmethod
                def list_feedback():
                    return list(fbs.find())

            print("Connected to MongoDB")
            return MongoWrapper
        except Exception as e:
            print("MongoDB not available, using InMemoryDB. Reason:", e)
    return InMemoryDB()