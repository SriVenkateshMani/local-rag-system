from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLm-L6-v2")

def generate_embeddings(texts):
    return model.encode(texts)