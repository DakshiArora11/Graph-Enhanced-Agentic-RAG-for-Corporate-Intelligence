import json
from pathlib import Path

def save_processed_data(text, entities, filename):
    """
    Save the extracted text and entities to a JSON file.
    
    Args:
        text (str): Extracted raw text from the PDF.
        entities (list): Extracted entities from the text.
        filename (str): The filename (usually the PDF's name) for the output JSON.
    """
    data = {
        "text": text,
        "entities": entities
    }
    output_path = Path(f"data/processed/{filename}.json")
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
