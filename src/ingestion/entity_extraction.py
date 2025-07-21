import os
from transformers import pipeline
import fitz  # PyMuPDF

# Set up NER model
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def enhance_entities(ner_results):
    # Merges nearby entities, filters invalid ones, and standardizes
    entities = []
    current = None
    for ent in ner_results:
        word = ent["word"].strip()
        label = ent["entity_group"]

        if current and current["label"] == label:
            current["text"] += f" {word}"
        else:
            if current:
                entities.append(current)
            current = {"text": word, "label": label}
    if current:
        entities.append(current)

    # Optional filtering (e.g., remove short terms or punctuation)
    enhanced = [e for e in entities if len(e["text"]) > 2 and e["text"].isprintable()]
    return enhanced

def extract_entities_from_pdf(pdf_path):
    file_name = os.path.basename(pdf_path)
    print(f"Processing file: {file_name}")

    # Step 1: Extract text
    text = extract_text_from_pdf(pdf_path)

    # Step 2: Apply NER
    ner_results = ner_pipeline(text)

    # Step 3: Enhance Entities
    enhanced_entities = enhance_entities(ner_results)

    # Step 4: Display
    print(f"\nEnhanced NER output from {file_name}:")
    for entity in enhanced_entities:
        print(f"Entity: {entity['text']}, Type: {entity['label']}")

# Example run
if __name__ == "__main__":
    pdf_path = "data/raw/AnnualReport_Amazon_24_form_10-K.pdf"
    extract_entities_from_pdf(pdf_path)
