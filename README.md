# RAG Document Assistant

A Retrieval-Augmented Generation (RAG) system for answering
questions over technical PDF documents.

## Architecture

PDF
→ Text Extraction
→ Chunking
→ Sentence Transformer Embeddings
→ PostgreSQL + pgvector
→ Semantic Retrieval
→ Context Construction
→ Gemini LLM
→ Grounded Answer with Sources

## Technologies

- Python
- PyMuPDF
- Sentence Transformers
- PostgreSQL
- pgvector
- Google Gemini
- psycopg

## How it works

1. A PDF is placed in the `data/` directory.
2. Text is extracted and divided into overlapping chunks.
3. Each chunk is converted into an embedding.
4. Embeddings and metadata are stored in PostgreSQL using pgvector.
5. A user's question is embedded using the same embedding model.
6. pgvector retrieves the most semantically similar chunks.
7. Retrieved chunks are supplied as context to Gemini.
8. Gemini generates an answer grounded in the retrieved document.
9. Source page numbers are included in the response.

## How to Use

This project allows you to upload a text-based PDF document, index it using
Sentence Transformer embeddings, store the embeddings in PostgreSQL with
pgvector, and ask questions about the document using Google Gemini.

### 1. Clone the Repository

```bash
git clone https://github.com/AmanTayal13/rag-project.git
cd rag-project
```
### 2. Set Up the Python Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```
### 3. Configure your Gemini API Key

Create a ```.env``` file in the project root:
```bash
GEMINI_API_KEY=your_api_key_here
```
### 4. Start PostGreSQL and pgvector
```bash
sudo docker run -d \
  --name pgvector \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=pswd \
  -e POSTGRES_DB=faq \
  -p 5432:5432 \
  -v pgvector_data:/var/lib/postgresql/data \
  pgvector/pgvector:pg17
```

If the container already exists but is stopped, use:
```bash
sudo docker start pgvector
```

### 5. Add Your PDF
Place your PDF inside:
```\data``` folder
The PDF should contain selectable/extractable text.

Scanned image-only PDFs are not currently supported.

### 6. Change PDF path
Open:
```index.py```
Find:
```bash
PDF_PATH = "data/<your-book.pdf>"
```

### 7. Ask a question
Inside ```index.py``` find:
```bash
query = "<YOUR-QUESTIOM>"
```
### 8. Run Index.py
Then run index.py
```bash
python index.py
```
