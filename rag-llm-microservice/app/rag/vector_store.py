import faiss
import numpy as np
import json
from typing import List, Tuple
import os

class VectorStore:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []
        
    def add_documents(self, embeddings: np.ndarray, documents: List[str]):
        """Add documents and their embeddings to the store"""
        self.index.add(embeddings)
        self.documents.extend(documents)
    
    def search(self, query_embedding: np.ndarray, k: int = 3) -> List[Tuple[str, float]]:
        """Search for similar documents"""
        query_embedding = query_embedding.reshape(1, -1)
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.documents):
                results.append((self.documents[idx], float(dist)))
        
        return results
    
    def load_documents(self, file_path: str):
        """Load documents from JSON file"""
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data.get('documents', [])
        return []