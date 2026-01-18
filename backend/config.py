"""
CourseCompanion - Configuration Settings
"""
import os
from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "CourseCompanion"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Mock Mode (offline/demo) - remove when not needed
    MOCK_MODE: bool = True  # lima-charli
    
    # Local Storage (replacing MongoDB)
    USE_LOCAL_STORAGE: bool = True
    STORAGE_DIR: str = "data/storage"
    
    # Azure OpenAI
    USE_AZURE_OPENAI: bool = True
    AZURE_OPENAI_API_KEY: str = ""
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"
    AZURE_OPENAI_DEPLOYMENT_NAME: str = ""  # Your GPT-4 deployment name
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME: str = ""  # Your embedding deployment name (optional)
    
    # Legacy OpenAI (fallback if not using Azure)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:8501",  # Streamlit default
        "http://localhost:3000",
        "http://127.0.0.1:8501",
        "http://127.0.0.1:3000"
    ]
    
    # Vector Search
    VECTOR_INDEX_NAME: str = "course_content_index"
    EMBEDDING_DIMENSIONS: int = 1536
    
    # RAG Settings
    RAG_CHUNK_SIZE: int = 1000
    RAG_CHUNK_OVERLAP: int = 200
    RAG_TOP_K: int = 5
    
    # Discovery Agent
    MAX_DISCOVERY_TURNS: int = 5
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Global settings instance
settings = get_settings()



