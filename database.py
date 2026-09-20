import psycopg


def get_connection():
    return psycopg.connect(
        "postgresql://user:pswd@localhost:5432/faq"
    )


def create_table(conn):
    conn.execute("""
        CREATE EXTENSION IF NOT EXISTS vector
    """)

    conn.execute("""
        DROP TABLE IF EXISTS documents
    """)

    conn.execute("""
        CREATE TABLE documents (
            id SERIAL PRIMARY KEY,
            document_name TEXT,
            page INTEGER,
            chunk_id INTEGER,
            content TEXT,
            embedding VECTOR(384)
        )
    """)

    conn.commit()


def vec_to_str(vector):
    return "[" + ",".join(str(x) for x in vector) + "]"


def insert_chunks(conn, chunks, document_name):
    for chunk in chunks:
        conn.execute(
            """
            INSERT INTO documents
                (document_name, page, chunk_id, content, embedding)
            VALUES
                (%s, %s, %s, %s, %s::vector)
            """,
            (
                document_name,
                chunk["page"],
                chunk["chunk_id"],
                chunk["text"],
                vec_to_str(chunk["embedding"])
            )
        )

    conn.commit()
    
def retrieve(conn, query, model, top_k=5):
    query_vector = model.encode(query)
    query_str = vec_to_str(query_vector)

    results = conn.execute("""
        SELECT
            content,
            page,
            chunk_id,
            embedding <=> %s::vector AS distance
        FROM documents
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """, (query_str, query_str, top_k)).fetchall()

    return results

def build_context(results):
    return "\n\n".join(
        f"[Page {row[1]}]\n{row[0]}"
        for row in results
    )