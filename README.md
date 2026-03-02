# Secure RAG API

A production-grade Retrieval-Augmented Generation (RAG) API system with enterprise security features.

## Overview

This microservice provides secure document ingestion, hybrid search (keyword + semantic), and LLM-powered Q&A capabilities. Built for enterprise internal knowledge management with role-based access control and audit logging.

### Key Features

- 🔐 **JWT Authentication** - Secure user authentication and authorization
- 📄 **Document Ingestion** - PDF, DOCX, TXT file processing
- 🔍 **Hybrid Search** - PostgreSQL full-text search + Qdrant vector similarity
- 🤖 **RAG Q&A** - LLM-powered answers with source citations
- 🔒 **Privacy-Aware** - Row-level security, user can only access their own documents
- 📊 **Audit Logging** - Track all document access for compliance
- ☁️ **AWS Integration** - S3 for document storage, EC2 deployment ready
- 🐳 **Dockerized** - Multi-container setup with docker-compose

## Tech Stack

- **API Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL (with full-text search)
- **Vector DB**: Qdrant
- **Object Storage**: AWS S3 (or MinIO for local dev)
- **LLM**: OpenAI GPT-4o-mini + text-embedding-3-small
- **Authentication**: JWT (python-jose)
- **Deployment**: Docker, AWS EC2

## Architecture

User → FastAPI API → PostgreSQL (metadata + full-text search) → Qdrant (vector embeddings) → S3 (raw documents) → OpenAI API (embeddings + chat)

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 15+
- OpenAI API key

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd secure-rag-api
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your actual values (OpenAI API key, database credentials, etc.)
```

### 5. Start databases with Docker Compose

```bash
docker-compose up -d postgres qdrant
```

### 6. Run database migrations

```bash
alembic upgrade head
```

### 7. Start the API server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 8. Access the API

- **API Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Project Structure

```
secure-rag-api/
├── app/
│   ├── api/              # API route handlers
│   ├── core/             # Configuration, security, dependencies
│   ├── models/           # SQLAlchemy ORM models
│   ├── schemas/          # Pydantic request/response models
│   ├── services/         # Business logic layer
│   └── db/               # Database connection utilities
├── tests/                # Unit and integration tests
├── docs/                 # Additional documentation
├── scripts/              # Utility scripts
├── .env.example          # Environment variable template
├── .gitignore            # Git ignore rules
├── requirements.txt      # Python dependencies
├── docker-compose.yml    # Multi-container setup
├── Dockerfile            # API container definition
└── README.md             # This file
```

## API Endpoints

### Authentication

- `POST /auth/register` - Create new user
- `POST /auth/login` - Login and get JWT token

### Documents

- `POST /documents/upload` - Upload and ingest document
- `GET /documents/{id}` - Retrieve document metadata
- `GET /documents/` - List user's documents
- `DELETE /documents/{id}` - Delete document

### Search

- `POST /search/query` - Hybrid search (keyword + vector)

### RAG

- `POST /rag/ask` - Ask questions, get LLM-powered answers with citations

### Health

- `GET /health` - API health check

## Development

### Run tests

```bash
pytest
```

### Format code

```bash
black app/ tests/
```

### Lint code

```bash
ruff check app/ tests/
```

### Run with hot reload

```bash
uvicorn app.main:app --reload
```

## Docker Deployment

### Build and run all services

```bash
docker-compose up -d
```

### View logs

```bash
docker-compose logs -f api
```

### Stop all services

```bash
docker-compose down
```

## AWS Deployment

See `docs/aws-deployment.md` for detailed EC2 deployment instructions.

## Security Considerations

- JWT tokens expire after 60 minutes
- Passwords are hashed with bcrypt (cost factor 12)
- Row-level security: users can only access their own documents or public ones
- S3 files are encrypted at rest (AES-256)
- Rate limiting: 60 requests per minute per user
- SQL injection prevented via parameterized queries
- CORS configured for specific origins only

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details