from src.embeddings import generate_embeddings

texts = [
    "Python is a programming language.",
    "OpenSearch supports vector search.",
    "RAG retrieves context before generation."
]

embeddings = generate_embeddings(texts)
