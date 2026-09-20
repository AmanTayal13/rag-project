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