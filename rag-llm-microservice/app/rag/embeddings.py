from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

class EmbeddingService:
    def __init__(self, model_name: str):
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for given texts"""
        return self.model.encode(texts, convert_to_numpy=True)
    
    def encode_query(self, query: str) -> np.ndarray:
        """Generate embedding for a single query"""
        return self.encode([query])[0]