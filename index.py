from sentence_transformers import SentenceTransformer

from ingestion import process_pdf
from database import get_connection, create_table, insert_chunks, retrieve, build_context
from rag import answer_question
from llm import llm

PDF_PATH = "data/<your-book.pdf>"

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Processing PDF...")
chunks = process_pdf(PDF_PATH, model)

print(f"Generated {len(chunks)} chunks.")

conn = get_connection()

print("Creating database table...")
create_table(conn)

print("Inserting chunks...")
insert_chunks(conn, chunks, "xv6-book")

print("Done")

query = "<YOUR-QUESTION>"

results = retrieve(conn, query, model)
    
context = build_context(results)

answer = answer_question(
    query,
    conn,
    model,
    llm
)

print("\nANSWER:")
print(answer)
