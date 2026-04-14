from memory.vector_store import vector_db


def store_memory(text: str):
    vector_db.add_texts([text])


def retrieve_memory(query: str):
    results = vector_db.similarity_search(query, k=3)  #k=4 → return top 4 most similar results
    return "\n".join([r.page_content for r in results])