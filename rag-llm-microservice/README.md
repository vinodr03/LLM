# RAG LLM Microservice

A secure microservice for question answering using RAG (Retrieval-Augmented Generation).

## Quick Start

1. Make sure Docker Desktop is running
2. Open Terminal in project directory
3. Run: `docker-compose up --build`
4. Visit: http://localhost:8000/docs

## Testing the API

Normal query:
- Question: "What is machine learning?"

Test security (these will be blocked):
- Question: "DROP TABLE users"
- Question: "ignore previous instructions"

## Features

- RAG-based question answering
- Security controls for prompt injection
- Comprehensive logging
- Docker containerization