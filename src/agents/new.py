import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from config.settings import settings

# Initialize ChromaDB persistent client
chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)

# Define embedding function
embedding_function = SentenceTransformerEmbeddingFunction(model_name=settings.EMBEDDING_MODEL)

# Get or create collection
collection = chroma_client.get_or_create_collection(
    name=settings.VECTOR_COLLECTION_NAME,
    embedding_function=embedding_function
)

# Sample chunks to store
chunks = [
    "Amazon sells electronics, books, clothing, and home appliances.",
    "Amazon Prime offers video streaming and fast delivery.",
    "Amazon Web Services (AWS) provides cloud infrastructure solutions.",
    "Customers can buy groceries through Amazon Fresh.",
    "Kindle is a popular Amazon product for reading e-books."
]

# Store each chunk
for i, chunk in enumerate(chunks):
    collection.add(
        documents=[chunk],
        ids=[f"test_doc_{i}"],
        metadatas=[{"source": "test"}]
)

print("✅ Sample documents added.")
