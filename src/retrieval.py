from src.opensearch_client import INDEX_NAME
from src.logger import get_logger

logger = get_logger(__name__)

# Build the semantic search using the vectors
def semantic_search(client, query_embedding, k):
    query = {
        "query":{
            "knn":{
                "embedding":{
                    "vector": query_embedding,
                    "k": k
                }
            }
        }
    }

    # Get the response with the afforementioned query 
    response = client.search(
        index = INDEX_NAME,
        body = query
    )

    return response

# Build the lexical search using the BM25
def lexical_search(client, query_text, k):
    query = {
        "query":{
            "match":{
                "text": query_text,
            },
        },
        "size": k
    }

    response = client.search(
        index = INDEX_NAME,
        body = query
    )

    return response


# Build Hybrid search using both semantic and lexical 
def hybrid_search(semantic_response, lexical_response, k):
    semantic_hits = semantic_response["hits"]["hits"]
    lexical_hits = lexical_response["hits"]["hits"]

    # Calculate fusion score
    fusion_scores = {}

    # Calculate rank for every hit of semantic search 
    for rank, hit in enumerate(semantic_hits, start = 1):
        document_id = hit["_id"]
        score = 1 / rank

        # Add the current score to the fusion score 
        fusion_scores[document_id] = score

    # Calculate rank for every hit of lexical search 
    for rank, hit in enumerate(lexical_hits, start = 1):
        document_id = hit["_id"]
        score = 1 / rank

        # Add the current score on top of the current fusion score
        fusion_scores[document_id] = fusion_scores.get(document_id, 0) + score

    # Sort the fusion dict in descending order in tuples list
    sorted_documents = sorted(
    fusion_scores.items(),
    key=lambda item: item[1],
    reverse=True
    )

    top_documents = sorted_documents[:k]

    documents_by_id = {}
    final_results = []

    # Store the document id for the full semantic hit
    for hit in semantic_hits:
        documents_by_id[hit["_id"]] = hit

    # Store the document id for the full lexical hit
    for hit in lexical_hits:
        documents_by_id[hit["_id"]] = hit

    # Get the hit for the top_documents 
    for document_id, fusion_score in top_documents:
        hit = documents_by_id[document_id]

        # Store the text and fusion score in a dict for the top docs
        result = {
            "id": document_id,
            "text": hit["_source"]["text"],
            "fusion_score": fusion_score
        }

        # Store the result in a list
        final_results.append(result)

    return final_results

