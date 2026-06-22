# vectordb.py
import chromadb
from sentence_transformers import SentenceTransformer
import os

class VectorDB:
    def __init__(self):
        # Initialize embedding model
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB (persistent storage)
        self.client = chromadb.PersistentClient(path="./chroma_db")
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="playbooks",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_playbook(self, playbook_key, content):
        """Add playbook content to vector database"""
        embedding = self.embedder.encode(content).tolist()
        
        self.collection.add(
            ids=[playbook_key],
            embeddings=[embedding],
            metadatas=[{"key": playbook_key}]
        )
    
    def search(self, query, n_results=2):
        """Search for most relevant playbooks"""
        query_embedding = self.embedder.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results
    
    def is_empty(self):
        return self.collection.count() == 0

# Initialize global instance
db = VectorDB()