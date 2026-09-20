from database import retrieve, build_context


def answer_question(query, conn, model, llm):

    results = retrieve(
        conn,
        query,
        model,
        top_k=5
    )

    context = build_context(results)

    prompt = f"""
Answer the user's question using ONLY the provided context.

Do not use your own knowledge.

If the context does not contain enough information to answer the question,
say that the information is insufficient.

Cite the relevant page numbers in your answer.

CONTEXT:
{context}

QUESTION:
{query}
"""

    return llm(
        "You are a document question-answering assistant.",
        prompt
    )