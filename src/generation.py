import ollama

def generate_answer(query, retrieved_chunks):

    # Create a string of all the chunks numbered
    context = ""
    for i, chunk in enumerate(retrieved_chunks, start = 1):
        context += f"\n[Chunk {i}]\n{chunk['text']}\n"

    # Talking with the LLM
    prompt = f"""
    Answer the question using only the context below.

    Context:
    {context}

    Question:
    {query}
    """

    # Generating response
    response = ollama.generate(
        model = "llama3.2:3b",
        prompt = prompt
    )

    # Response generates a dict, so extracting just the answer
    answer = response["response"]

    return answer