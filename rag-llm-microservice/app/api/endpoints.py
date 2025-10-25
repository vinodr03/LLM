from fastapi import APIRouter, HTTPException, Request
from app.models import QueryRequest, QueryResponse
from app.rag.retriever import RAGRetriever
from app.llm.generator import LLMGenerator
from app.security.prompt_guard import PromptGuard
from app.security.logger import SecurityLogger
from app.config import settings
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services (will be done on first request)
retriever = None
generator = None
prompt_guard = None
security_logger = None

def get_services():
    global retriever, generator, prompt_guard, security_logger
    if retriever is None:
        print("Initializing services...")
        retriever = RAGRetriever()
        generator = LLMGenerator()
        prompt_guard = PromptGuard()
        security_logger = SecurityLogger()
        print("Services initialized!")
    return retriever, generator, prompt_guard, security_logger

@router.post("/query", response_model=QueryResponse)
async def process_query(request: Request, query: QueryRequest):
    """Process user query with RAG and security checks"""
    
    # Initialize services if needed
    retriever, generator, prompt_guard, security_logger = get_services()
    
    # Get client IP
    client_ip = request.client.host if request.client else "unknown"
    
    # Security check
    is_safe, reason = prompt_guard.check_prompt(query.question)
    
    if not is_safe:
        # Log flagged query
        security_logger.log_query(
            query=query.question,
            flagged=True,
            reason=reason,
            ip=client_ip
        )
        
        raise HTTPException(
            status_code=400,
            detail=f"Query flagged for security reasons: {reason}"
        )
    
    try:
        # Retrieve relevant contexts
        contexts = retriever.retrieve(query.question, k=settings.top_k_results)
        
        # Generate response
        answer = generator.generate_response(query.question, contexts)
        
        # Sanitize response
        answer = prompt_guard.sanitize_response(answer)
        
        # Create response
        response = QueryResponse(
            answer=answer,
            contexts=contexts,
            query_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            flagged=False
        )
        
        # Log successful query
        security_logger.log_query(
            query=query.question,
            flagged=False,
            response=answer,
            ip=client_ip
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}