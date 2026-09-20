import re
import pymupdf
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


def extract_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)

    pages = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text().strip()

        if text:
            pages.append({
                "page": page_num,
                "text": text
            })

    doc.close()
    return pages


def clean_text(text):
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text, chunk_size=2000, overlap=300):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks


def process_pdf(pdf_path, model):
    pages = extract_pdf(pdf_path)

    chunks = []

    for page in pages:
        text = clean_text(page["text"])

        page_chunks = chunk_text(text)

        for chunk in page_chunks:
            chunks.append({
                "page": page["page"],
                "text": chunk
            })

    # Generate embeddings

    for chunk in tqdm(chunks, desc="Embedding chunks"):
        chunk["embedding"] = model.encode(chunk["text"]).tolist()

    # Add chunk IDs
    for chunk_id, chunk in enumerate(chunks):
        chunk["chunk_id"] = chunk_id

    return chunks