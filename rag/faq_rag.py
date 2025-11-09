from rag.vector_store import load_vector_store


def retrieve_insurance_info(query: str, k: int = 3):
    """
    Retrieves top-k relevant chunks from the insurance vector store.
    """
    vectordb = load_vector_store()
    results = vectordb.similarity_search(query, k=k)

    if not results:
        return "No relevant information found."

    context = "\n\n".join([r.page_content for r in results])
    return context


if __name__ == "__main__":
    print(retrieve_insurance_info("Does my insurance cover hospitalization?"))
