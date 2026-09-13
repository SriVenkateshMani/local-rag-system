from opensearchpy import OpenSearch
from src.logger import get_logger

logger = get_logger(__name__)

def get_opensearch_client():
    client = OpenSearch(
        hosts = [{
            "host": "localhost",
            "port": 9200
        }]
    )
    return client

INDEX_NAME = "rag_documents"

# Define an index body (schema of how it looks)
index_body = {
    "mappings":{
        "properties":{
            "text":{
                "type": "text"
            },
            "embedding":{
                "type": "knn_vector",
                "dimension": 384
            }
        }
    },
    "settings":{
        "index":{
            "knn": True
        }
    }
}

# Create an opensearch Index
def create_index(client):
    if not client.indices.exists(index = INDEX_NAME):
        client.indices.create(
            index = INDEX_NAME,
            body = index_body
        )

