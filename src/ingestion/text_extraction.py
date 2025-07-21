import os
from transformers import pipeline
import fitz  # PyMuPDF

# Initialize Hugging Face pipeline for NER
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)

def extract_text_from_pdf(file_path):
    """Extract full text from a PDF file using PyMuPDF."""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def basic_clean_ner_output(ner_results):
    """Clean grouped NER output by combining entity words."""
    entities = []
    for ent in ner_results:
        word = ent.get("word", "").replace("##", "").strip()
        entity_group = ent.get("entity_group", "UNKNOWN")
        if not word:
            continue
        entities.append({
            "word": word,
            "entity_group": entity_group
        })
    return entities

def extract_entities_from_pdf(pdf_path):
    file_name = os.path.basename(pdf_path)
    print(f"📄 Processing file: {file_name}")

    # Step 1: Extract text
    text = extract_text_from_pdf(pdf_path)

    # Step 2: Apply NER model
    ner_results = ner_pipeline(text)

    # Step 3: Clean output
    cleaned_entities = basic_clean_ner_output(ner_results)

    # Step 4: Display entities
    print(f"\n🔎 Named Entities extracted from {file_name}:\n")
    for entity in cleaned_entities:
        print(f"Entity: {entity['word']}, Type: {entity['entity_group']}")

if __name__ == "__main__":
    pdf_path = "AnnualReport_Amazon_24_form_10-K.pdf"
    extract_entities_from_pdf(pdf_path)
