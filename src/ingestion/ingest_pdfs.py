# src/ingestion/ingest_pdfs.py
from src.ingestion.text_extraction import extract_text_from_pdf
from src.ingestion.relation_extraction import extract_triplets
from src.storage.vector_store import store_text_chunks
from src.storage.graph_store import GraphStore
from src.utils.text_utils import split_text
import os
from config.settings import settings

def ingest_pdfs():
    graph_store = GraphStore()
    pdf_dir = settings.RAW_DATA_DIR
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, filename)
            print(f"Processing {filename}")
            text = extract_text_from_pdf(pdf_path)
            if text:
                # Split and store text chunks in ChromaDB
                chunks = split_text(text, settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)
                store_text_chunks(chunks, filename)
                print(f"Stored {len(chunks)} chunks from {filename} in ChromaDB.")
                # Extract and store triplets in Neo4j
                triplets = extract_triplets(text)
                for subject, predicate, obj in triplets:
                    graph_store.create_triplet(subject, predicate, obj)
                print(f"Stored {len(triplets)} triplets from {filename} in Neo4j.")
            else:
                print(f"No text extracted from {filename}")

if __name__ == "__main__":
    ingest_pdfs()