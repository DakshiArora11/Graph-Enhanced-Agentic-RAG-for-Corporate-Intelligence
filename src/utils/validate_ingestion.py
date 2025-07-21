# src/utils/validate_ingestion.py
from src.storage.vector_store import client as chroma_client
from src.storage.graph_store import GraphStore
from config.settings import settings

def validate_ingestion():
    # Check ChromaDB
    collection = chroma_client.get_collection(name=settings.VECTOR_COLLECTION_NAME)
    count = collection.count()
    print(f"ChromaDB contains {count} documents.")

    # Check Neo4j
    graph_store = GraphStore()
    result = graph_store.query_triplets("")  # Query all triplets
    print(f"Neo4j contains {len(result)} triplets.")

if __name__ == "__main__":
    validate_ingestion()