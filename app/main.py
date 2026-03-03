"""
Main FastAPI application entry point.

This file:
1. Creates the FastAPI application instance
2. Configures CORS middleware
3. Registers API routes
4. Sets up startup/shutdown event handlers
5. Provides health check endpoint
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    """
    Application factory pattern.
    
    Creates and configures a FastAPI application instance.
    This pattern allows creating multiple app instances (useful for testing).
    
    Returns:
        FastAPI: Configured FastAPI application
    """
    
    # Create FastAPI instance with metadata
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="""
        ## Secure RAG API
        
        A production-grade Retrieval-Augmented Generation system with enterprise security.
        
        ### Features
        * 🔐 JWT Authentication
        * 📄 Document ingestion (PDF, DOCX, TXT)
        * 🔍 Hybrid search (keyword + vector)
        * 🤖 LLM-powered Q&A with citations
        * 🔒 Role-based access control
        * 📊 Audit logging
        
        ### Authentication
        Most endpoints require a JWT token. Obtain one by:
        1. Register: `POST /auth/register`
        2. Login: `POST /auth/login`
        3. Use the token in the `Authorization: Bearer <token>` header
        """,
        docs_url="/docs" if settings.DEBUG else None,  # Disable docs in production
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
    )
    
    # Configure CORS (Cross-Origin Resource Sharing)
    # Allows frontend apps from specified origins to call this API
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,  # Which domains can access
        allow_credentials=True,               # Allow cookies/auth headers
        allow_methods=["*"],                  # Allow all HTTP methods (GET, POST, etc.)
        allow_headers=["*"],                  # Allow all headers
    )
    
    return application


# Create the FastAPI app instance
app = create_application()


# Startup event: Runs once when the server starts
@app.on_event("startup")
async def startup_event():
    """
    Initialize resources on application startup.
    
    This runs once when uvicorn starts the server.
    Use this for:
    - Database connection pool initialization
    - Loading ML models into memory
    - Warming up caches
    - Connecting to external services
    """
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # TODO: Initialize database connection pool
    # TODO: Initialize Qdrant client
    # TODO: Verify OpenAI API key is valid
    
    logger.info("Application startup complete")


# Shutdown event: Runs once when the server stops
@app.on_event("shutdown")
async def shutdown_event():
    """
    Cleanup resources on application shutdown.
    
    This runs when you stop the server (Ctrl+C) or during graceful shutdown.
    Use this for:
    - Closing database connections
    - Flushing logs/metrics
    - Saving state
    """
    logger.info("Shutting down application...")
    
    # TODO: Close database connections
    # TODO: Close Qdrant connection
    # TODO: Flush any pending logs
    
    logger.info("Application shutdown complete")


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for load balancers and monitoring.
    
    Returns:
        dict: Application health status
        
    Example response:
        {
            "status": "healthy",
            "app_name": "Secure RAG API",
            "version": "1.0.0",
            "environment": "development"
        }
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
        }
    )


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        dict: Welcome message and links to documentation
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.DEBUG else "Documentation disabled in production",
        "health": "/health",
    }


# TODO: Register API routers here
# Example:
# from app.api.routes import auth, documents, search, rag
# app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# app.include_router(documents.router, prefix="/documents", tags=["Documents"])
# app.include_router(search.router, prefix="/search", tags=["Search"])
# app.include_router(rag.router, prefix="/rag", tags=["RAG"])


if __name__ == "__main__":
    # This allows running with: python -m app.main
    # For development only - in production, use: uvicorn app.main:app
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,  # Auto-reload on code changes (dev only)
        log_level=settings.LOG_LEVEL.lower(),
    )
