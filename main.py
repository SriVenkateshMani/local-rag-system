from src.embeddings import generate_embeddings
from src.logger import get_logger
from sentence_transformers import util
from src.ingestion import index_document
from src.opensearch_client import create_index, get_opensearch_client
from src.retrieval import semantic_search

logger = get_logger(__name__)

texts = [
    "Python is a programming language.",
    "OpenSearch supports vector search.",
    "RAG retrieves context before generation."
]

query = "Give me a programming language"

query_embedding = generate_embeddings([query])

embeddings = generate_embeddings(texts)
similarities = util.cos_sim(query_embedding, embeddings)

# Build open search document list
# Open search compatible to retrieve
documents = []
for text, embedding in zip(texts, embeddings):
    document = {}
    document["text"] = text
    document["embedding"] = embedding.tolist()

    documents.append(document)


# Index the documents in Opensearch Indices
client = get_opensearch_client()
create_index(client)

for doc in documents:
    index_document(client, doc)

# Query embedding is numpy arr, so changing to python list
response = semantic_search(client, query_embedding[0].tolist(), k = 3)

logger.info(len(response["hits"]["hits"]))