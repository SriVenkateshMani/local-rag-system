# Local Hybrid RAG System

A local Retrieval-Augmented Generation (RAG) system built from scratch to understand the core components behind modern RAG pipelines.

The project uses **Sentence Transformers** for embeddings and **OpenSearch** as the retrieval backend, with the goal of supporting both **semantic vector search** and **BM25 lexical search**, followed by hybrid retrieval and local LLM generation.

## Why This Project?

RAG frameworks such as LangChain and LlamaIndex provide convenient abstractions for retrieval pipelines. This project intentionally implements the core retrieval workflow directly to understand what happens underneath those abstractions.

The system is being built incrementally:

```text
Documents
    ↓
Chunking
    ↓
Embeddings
    ↓
OpenSearch
    ├── Dense Vector Search
    └── BM25 Lexical Search
            ↓
      Hybrid Retrieval
            ↓
        Local LLM
            ↓
         Response
```

## Current Progress

- [x] Project structure and logging
- [x] Sentence Transformer embeddings
- [x] OpenSearch running locally with Docker
- [x] OpenSearch index and vector mapping
- [x] Document ingestion with deterministic IDs
- [x] Dense semantic retrieval using k-NN
- [ ] BM25 lexical retrieval
- [ ] Hybrid search
- [ ] Document/PDF ingestion and chunking
- [ ] Local LLM integration
- [ ] RAG response generation
- [ ] Streamlit interface

## Tech Stack

- **Python**
- **Sentence Transformers**
- **OpenSearch**
- **Docker / Docker Compose**
- **Local LLM** — planned
- **Streamlit** — planned

## Project Structure

```text
local-rag-system/
├── src/
│   ├── __init__.py
│   ├── embeddings.py
│   ├── ingestion.py
│   ├── logger.py
│   ├── opensearch_client.py
│   └── retrieval.py
├── .gitignore
├── docker-compose.yml
├── main.py
├── requirements.txt
└── README.md
```

### Module Responsibilities

`embeddings.py`
: Generates vector embeddings from text using Sentence Transformers.

`opensearch_client.py`
: Creates the OpenSearch client and defines the index configuration and mappings.

`ingestion.py`
: Stores documents and their embeddings in OpenSearch using deterministic document IDs.

`retrieval.py`
: Contains retrieval logic, including semantic k-NN search and eventually BM25 and hybrid retrieval.

`logger.py`
: Provides centralized application logging.

`main.py`
: Orchestrates embedding generation, ingestion, and retrieval.

## Retrieval

### Dense Semantic Search

Queries are converted into embeddings using the same embedding model used for the indexed documents.

```text
Query
  ↓
Sentence Transformer
  ↓
Query Embedding
  ↓
OpenSearch k-NN Search
  ↓
Top-K Semantically Similar Documents
```

This allows retrieval based on semantic meaning rather than only exact keyword matches.

### BM25 Lexical Search

Coming next.

BM25 will search the `text` field using lexical relevance, allowing the system to retrieve documents based on matching words and terms.

### Hybrid Search

The final retriever will combine:

```text
Dense Search  ──┐
                ├── Hybrid Ranking → Top-K Context
BM25 Search   ──┘
```

This combines semantic similarity with traditional keyword-based retrieval.

## Running OpenSearch

Start the local OpenSearch server:

```bash
docker compose up
```

Verify that OpenSearch is running:

```bash
curl http://localhost:9200
```

## Running the Project

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

## Security

Secrets and local environment variables should be stored in `.env` and must not be committed to Git.

The `.gitignore` includes local development files such as:

```text
venv/
__pycache__/
.env
```

Never commit API keys or other credentials to the repository.

## Learning Goals

This project focuses on understanding the individual pieces of a RAG system rather than relying entirely on high-level framework abstractions.

Key concepts explored include:

- Text embeddings
- Vector similarity search
- k-nearest neighbors (k-NN)
- OpenSearch mappings and indexing
- Dense retrieval
- BM25 lexical retrieval
- Hybrid retrieval
- Document chunking
- Retrieval-Augmented Generation
- Local LLM inference

## Status

🚧 **Work in progress**

The dense semantic retrieval pipeline is currently functional. BM25 retrieval, hybrid search, real document ingestion, and generation are being added incrementally.
