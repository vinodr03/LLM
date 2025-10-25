from typing import List, Tuple
from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore
from app.config import settings

class RAGRetriever:
    def __init__(self):
        print("Initializing RAG Retriever...")
        self.embedding_service = EmbeddingService(settings.embedding_model)
        self.vector_store = VectorStore(settings.vector_dim)
        self._initialize_store()
    
    def _initialize_store(self):
        """Initialize vector store with documents"""
        print("Loading documents...")
        documents = self.vector_store.load_documents('data/documents/sample_docs.json')
        if documents:
            print(f"Encoding {len(documents)} documents...")
            embeddings = self.embedding_service.encode(documents)
            self.vector_store.add_documents(embeddings, documents)
            print("Documents loaded successfully!")
    
    def retrieve(self, query: str, k: int = 3) -> List[str]:
        """Retrieve relevant documents for a query"""
        query_embedding = self.embedding_service.encode_query(query)
        results = self.vector_store.search(query_embedding, k)
        return [doc for doc, _ in results]