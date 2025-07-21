import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from config.settings import settings

# Define proper embedding function object
embedding_function = SentenceTransformerEmbeddingFunction(model_name=settings.EMBEDDING_MODEL)

client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)

collection = client.get_or_create_collection(
    name=settings.VECTOR_COLLECTION_NAME,
    embedding_function=embedding_function
)

# Store chunks function
def store_text_chunks(chunks, source_doc):
    for i, chunk in enumerate(chunks):
        chunk_id = f"{source_doc}_{i}"
        collection.add(
            documents=[chunk],
            ids=[chunk_id],
            metadatas=[{"source": source_doc}]
        )
    print(f"Stored {len(chunks)} chunks from {source_doc} in ChromaDB.")
