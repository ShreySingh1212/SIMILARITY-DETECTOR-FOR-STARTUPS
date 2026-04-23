# 🔍 IdeaLens — Startup Idea Similarity Detector

AI-powered tool that analyzes your startup idea against 100+ real companies to find similar startups, compute a uniqueness score, and provide competitive gap analysis.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vite + React |
| Styling | Vanilla CSS (glassmorphism dark theme) |
| Backend | FastAPI (Python) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector DB | ChromaDB (local) |
| LLM | Groq API (Llama 3 70B) |
| Database | SQLite + SQLAlchemy |

## Quick Start

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

## Features

- **Semantic Similarity** — AI embeddings understand meaning, not just keywords
- **Uniqueness Score** — 0-100% rating of how unique your idea is
- **100+ Startups** — Compared against real companies across 20+ categories
- **AI Gap Analysis** — Powered by Groq Llama 3 for competitive insights
- **Premium UI** — Dark glassmorphism design with smooth animations
