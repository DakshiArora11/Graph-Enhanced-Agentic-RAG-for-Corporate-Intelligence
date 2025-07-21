# src/ingestion/relation_extraction.py
from transformers import pipeline

nlp = pipeline("ner", model="dslim/bert-base-NER")
relation_model = pipeline("text2text-generation", model="google/flan-t5-base")

def extract_triplets(text):
    entities = nlp(text)
    triplets = []
    for i in range(len(entities) - 1):
        subject = entities[i]['word']
        for j in range(i + 1, len(entities)):
            predicate = "sell"  # Simplify for now; use relation_model for better predicates
            obj = entities[j]['word']
            if subject.lower() in text.lower() and obj.lower() in text.lower():
                triplets.append((subject, predicate, obj))
    return triplets