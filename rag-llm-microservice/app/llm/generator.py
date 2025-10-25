from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
from typing import List
from app.config import settings

class LLMGenerator:
    def __init__(self):
        print(f"Loading LLM model: {settings.llm_model}")
        self.model_name = settings.llm_model
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        print(f"Model loaded on {self.device}")
    
    def generate_response(self, query: str, contexts: List[str]) -> str:
        """Generate response using RAG"""
        # Prepare context
        context_text = "\n".join(contexts[:2])  # Limit context to avoid token limits
        
        # Create prompt
        prompt = f"Answer based on context: {context_text}\nQuestion: {query}\nAnswer:"
        
        # Tokenize
        inputs = self.tokenizer(
            prompt, 
            max_length=512,
            truncation=True,
            return_tensors="pt"
        ).to(self.device)
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=100,
                temperature=0.7,
                do_sample=True,
                top_p=0.9
            )
        
        # Decode
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response