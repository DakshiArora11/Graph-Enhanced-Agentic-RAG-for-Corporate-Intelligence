# src/agents/vector_query.py
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from config.settings import settings
embedding_function = SentenceTransformerEmbeddingFunction(model_name=settings.EMBEDDING_MODEL)

import tempfile
import os
import chromadb
temp_dir = os.path.join(tempfile.gettempdir(), "chroma_db")
os.makedirs(temp_dir, exist_ok=True)  # Ensure directory exists
client = chromadb.PersistentClient(path=temp_dir)

collection = client.get_or_create_collection(
    name=settings.VECTOR_COLLECTION_NAME,
    embedding_function=embedding_function
)

def query_chromadb(query: str, top_k: int = 5):
    global collection
    if not collection:
        print("[Vector Query Warning] Collection is not initialized.")
        return []
    try:
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )
        documents = results['documents'][0] if results and 'documents' in results else []
        print(f"Retrieved {len(documents)} documents: {documents}")
        return documents
    except Exception as e:
        print(f"[Vector Query Error] {e}")
        return []