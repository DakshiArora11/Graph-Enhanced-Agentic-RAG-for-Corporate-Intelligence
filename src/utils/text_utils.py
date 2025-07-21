# src/utils/text_utils.py
def split_text(text, chunk_size=1000, chunk_overlap=200):
    chunks = []
    for i in range(0, len(text), chunk_size - chunk_overlap):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
    return chunks