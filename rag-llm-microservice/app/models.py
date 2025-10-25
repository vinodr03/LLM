from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    
    @validator('question')
    def validate_question(cls, v):
        if not v.strip():
            raise ValueError("Question cannot be empty")
        return v.strip()

class QueryResponse(BaseModel):
    answer: str
    contexts: List[str]
    query_id: str
    timestamp: datetime
    flagged: bool = False

class SecurityLog(BaseModel):
    timestamp: datetime
    query: str
    flagged: bool
    reason: Optional[str]
    response: Optional[str]
    ip_address: Optional[str]