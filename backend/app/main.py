from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router as api_v1_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="TaskLine - A simple and powerful To-Do List API",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Root endpoint - health check"""
    return {"message": "Welcome to TaskLine API!", "docs": "/docs"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "project": settings.PROJECT_NAME}

app.include_router(api_v1_router, prefix="/api/v1")
