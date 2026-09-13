from src.opensearch_client import INDEX_NAME
from src.logger import get_logger

logger = get_logger(__name__)

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