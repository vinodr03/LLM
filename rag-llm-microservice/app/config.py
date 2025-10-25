from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # API Settings
    api_title: str = "RAG LLM Microservice"
    api_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Model Settings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    llm_model: str = "google/flan-t5-small"  # Using small model for speed
    max_context_length: int = 512
    max_response_length: int = 256
    
    # Security Settings
    max_prompt_length: int = 1000
    blocked_patterns: List[str] = [
        "ignore previous instructions",
        "disregard all",
        "system prompt",
        "DROP TABLE",
        "SELECT * FROM",
        "exec(",
        "eval(",
        "__import__",
        "os.system",
        "subprocess"
    ]
    
    # Vector Store Settings
    vector_dim: int = 384
    top_k_results: int = 3
    
    class Config:
        env_file = ".env"

settings = Settings()