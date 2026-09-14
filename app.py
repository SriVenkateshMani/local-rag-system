import streamlit as st

from src.document_loader import load_pdf, chunk_text
from src.embeddings import generate_embeddings
from src.opensearch_client import get_opensearch_client, create_index
from src.ingestion import index_document
from src.retrieval import semantic_search, lexical_search, hybrid_search
from src.generation import generate_answer


st.title("Local Hybrid RAG System")

if "indexed_file" not in st.session_state:
    st.session_state.indexed_file = None

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    client = get_opensearch_client()
    create_index(client)

    # Only process the PDF if it has not already been indexed
    if st.session_state.indexed_file != uploaded_file.name:

        pdf_text = load_pdf(uploaded_file)

        texts = chunk_text(pdf_text)

        embeddings = generate_embeddings(texts)

        documents = []

        for text, embedding in zip(texts, embeddings):
            document = {
                "text": text,
                "embedding": embedding.tolist()
            }

            documents.append(document)

        for doc in documents:
            index_document(client, doc)

        client.indices.refresh(index="rag_documents")

        st.session_state.indexed_file = uploaded_file.name

        st.success("PDF processed and indexed successfully.")

    query = st.text_input("Ask a question about the PDF")

    if query:
        query_embedding = generate_embeddings([query])

        semantic_response = semantic_search(
            client,
            query_embedding[0].tolist(),
            k=3
        )

        bm25_response = lexical_search(
            client,
            query,
            k=3
        )

        hybrid_response = hybrid_search(
            semantic_response,
            bm25_response,
            k=3
        )

        answer = generate_answer(
            query,
            hybrid_response
        )

        st.subheader("Answer")
        st.write(answer)