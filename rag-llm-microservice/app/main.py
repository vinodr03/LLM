from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router
from app.config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1", tags=["queries"])

@app.get("/")
async def root():
    return {
        "message": "RAG LLM Microservice",
        "version": settings.api_version,
        "docs": "/docs"
    }

@app.on_event("startup")
async def startup_event():
    print("Starting RAG LLM Microservice...")
    print(f"Documentation available at: http://localhost:8000/docs")