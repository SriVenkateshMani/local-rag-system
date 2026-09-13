from src.embeddings import generate_embeddings
from src.logger import get_logger
from sentence_transformers import util
from src.ingestion import index_document
from src.opensearch_client import create_index, get_opensearch_client
from src.retrieval import semantic_search, lexical_search, hybrid_search
from src.document_loader import load_pdf, chunk_text
from src.generation import generate_answer

logger = get_logger(__name__)

pdf_text = load_pdf("data/sample_rag_knowledge_base.pdf")
texts = chunk_text(pdf_text)

logger.info(f"Created {len(texts)} chunks")
logger.info(texts[0][:500])
query = "How does hybrid search combine BM25 and semantic retrieval?"
query_embedding = generate_embeddings([query])

embeddings = generate_embeddings(texts)

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
semantic_response = semantic_search(client, query_embedding[0].tolist(), k = 3)

# Calling lexical search
bm25_response = lexical_search(client, query, k = 3)

# Calling hybrid search
hybrid_response = hybrid_search(semantic_response, bm25_response, k = 3)

# Generate an answer with LLM
answer = generate_answer(query, hybrid_response)
logger.info(answer)