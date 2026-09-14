# Local Hybrid RAG System

A local Retrieval-Augmented Generation system built from scratch using OpenSearch, Sentence Transformers, Ollama, and Streamlit.

The application allows users to upload a PDF, retrieve the most relevant sections using both semantic vector search and BM25 keyword search, combine both result sets using reciprocal-rank fusion, and generate an answer locally using Llama 3.2 through Ollama.

## Why This Project?

I built this project to understand what actually happens inside a RAG pipeline instead of relying immediately on frameworks like LangChain or LlamaIndex.

The goal was to learn each stage independently:

- How documents are extracted and chunked
- How embeddings are generated
- How vector similarity search works
- How BM25 keyword retrieval differs from semantic retrieval
- Why hybrid retrieval can outperform either approach alone
- How retrieved context is passed to an LLM
- How retrieval quality directly affects answer quality
- How to run an entire RAG pipeline locally

Building the pipeline manually made it much easier to understand where retrieval latency, bad answers, duplicate indexing, chunking issues, and ranking problems actually come from.

## Architecture

```text
PDF Upload
    ↓
Text Extraction
    ↓
Word-Based Chunking
    ↓
SentenceTransformer Embeddings
    ↓
OpenSearch
    ├── BM25 Lexical Search
    └── k-NN Semantic Search
             ↓
     Reciprocal-Rank Fusion
             ↓
      Top Relevant Chunks
             ↓
       Prompt Construction
             ↓
          Ollama
             ↓
       Llama 3.2 3B
             ↓
           Answer
```

## Hybrid Search

The main focus of this project is hybrid retrieval.

Instead of relying only on vector similarity, each user query is processed through two retrieval methods.

**BM25 Search** finds chunks containing important exact words and phrases.

**Semantic Search** converts the query into an embedding and retrieves chunks with similar meaning using OpenSearch k-NN vector search.

The rankings from both searches are combined using reciprocal-rank fusion.

```text
BM25
exact keyword relevance

        +

Semantic Search
meaning-based relevance

        ↓

Hybrid Retrieval
```

This helps the system handle both exact technical terms and questions where the wording differs from the original document.

## Tech Stack

- Python
- Streamlit
- OpenSearch
- Docker
- Sentence Transformers
- `all-MiniLM-L6-v2`
- BM25
- k-NN Vector Search
- Reciprocal-Rank Fusion
- Ollama
- Llama 3.2 3B
- pypdf

## Project Structure

```text
local-rag-system/
├── .streamlit/
│   └── config.toml
├── data/
│   └── sample_rag_knowledge_base.pdf
├── src/
│   ├── __init__.py
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── generation.py
│   ├── ingestion.py
│   ├── logger.py
│   ├── opensearch_client.py
│   └── retrieval.py
├── app.py
├── main.py
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/local-rag-system.git
cd local-rag-system
```

### 2. Create a virtual environment

```bash
python3 -m venv ~/.venvs/local-rag-system
source ~/.venvs/local-rag-system/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start OpenSearch with Docker

```bash
docker compose up -d
```

Verify OpenSearch:

```bash
curl http://localhost:9200
```

OpenSearch should be running at:

```text
http://localhost:9200
```

### 5. Install the local LLM

Install Ollama and pull the model:

```bash
ollama pull llama3.2:3b
```

Verify:

```bash
ollama list
```

### 6. Run the application

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

Upload a text-based PDF and ask questions about it.

## How the Full Pipeline Works

When a PDF is uploaded:

```text
PDF
→ extract text
→ split into overlapping chunks
→ generate 384-dimensional embeddings
→ store chunks and embeddings in OpenSearch
```

When a question is asked:

```text
Question
→ generate query embedding
→ semantic k-NN search
→ BM25 search
→ fuse both rankings
→ select top chunks
→ send retrieved context to Llama
→ generate grounded answer
```

The embeddings are generated with `all-MiniLM-L6-v2`, while OpenSearch handles both BM25 and vector retrieval.

Ollama runs `llama3.2:3b` locally for answer generation.

The Streamlit UI is intentionally simple and most of the work went into understanding and implementing the retrieval pipeline rather than frontend styling. Also don't bash me for not deploying it, again the same reason sorry folks :)

## Author

**Sri Venkatesha Mani**
