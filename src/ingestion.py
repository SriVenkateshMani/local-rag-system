from src.opensearch_client import INDEX_NAME
import hashlib


# The real indexing of contents 
def index_document(client, document):
    # Gets the text, turns strings into bytes, creates hash, gives hexadecimal string
    document_id = hashlib.sha256(document["text"].encode()).hexdigest()
    client.index(
        index = INDEX_NAME,
        id = document_id,
        body = document
    )