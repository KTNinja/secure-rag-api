"""
Configuration management using Pydantic Settings.

Loads settings from environment variables (from .env file or system environment).
Provides type-safe, validated configuration throughout the application.
"""

from typing import List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import json


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings can be overridden by setting environment variables.
    For example, DATABASE_URL in .env will override the default below.
    """
    
    # Application
    APP_NAME: str = "Secure RAG API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Security
    SECRET_KEY: str = Field(..., min_length=32)  # Required, minimum 32 chars
    JWT_SECRET_KEY: str = Field(..., min_length=32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Database (PostgreSQL)
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/secure_rag_db"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "secure_rag_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    
    # Vector Database (Qdrant)
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION_NAME: str = "documents"
    
    # AWS S3
    AWS_ACCESS_KEY_ID: str = "your-aws-access-key"
    AWS_SECRET_ACCESS_KEY: str = "your-aws-secret-key"
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "secure-rag-documents"
    USE_LOCAL_STORAGE: bool = True  # Use local filesystem instead of S3 for dev
    
    # OpenAI
    OPENAI_API_KEY: str = Field(..., min_length=20)  # Required
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    OPENAI_CHAT_MODEL: str = "gpt-4o-mini"
    EMBEDDING_DIMENSION: int = 1536
    
    # CORS (Cross-Origin Resource Sharing)
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Pydantic Settings Configuration
    model_config = SettingsConfigDict(
        env_file=".env",           # Load from .env file
        env_file_encoding="utf-8",
        case_sensitive=True,       # Environment variable names are case-sensitive
        extra="ignore"             # Ignore extra fields in .env
    )
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """
        Parse CORS_ORIGINS from string to list.
        
        Allows setting CORS_ORIGINS as JSON string in .env:
        CORS_ORIGINS='["http://localhost:3000"]'
        """
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # If not valid JSON, split by comma
                return [origin.strip() for origin in v.split(",")]
        return v
    
    @property
    def database_url_async(self) -> str:
        """
        Async database URL for SQLAlchemy.
        
        SQLAlchemy 2.0 with asyncpg driver requires postgresql+asyncpg://
        """
        return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT.lower() == "production"
    
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT.lower() == "development"


# Create a single global settings instance
# This is loaded once at startup and reused throughout the application
settings = Settings()


# For debugging: print loaded settings (excluding secrets)
if __name__ == "__main__":
    print("=== Configuration Loaded ===")
    print(f"App Name: {settings.APP_NAME}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"Database: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    print(f"Qdrant: {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")
    print(f"OpenAI Model: {settings.OPENAI_CHAT_MODEL}")
    print(f"CORS Origins: {settings.CORS_ORIGINS}")
    print(f"Is Production: {settings.is_production()}")
    print("=============================")
