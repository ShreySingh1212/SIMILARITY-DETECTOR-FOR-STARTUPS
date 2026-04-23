"""
FastAPI main application - Startup Idea Similarity Detector
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
import logging

from app.config import settings
from app.database import init_db, SessionLocal, get_db
from app.models import User, SearchHistory
from app.schemas import (
    AnalyzeRequest, AnalyzeResponse, HealthResponse, StartupInfo,
    RegisterRequest, LoginRequest, TokenResponse, UserResponse,
    HistoryItem, HistoryResponse
)
from app.auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, get_optional_user
)
from app.embedder import embedder
from app.vector_store import vector_store
from app.similarity import (
    process_search_results, compute_uniqueness_score, get_category_distribution
)
from app.gap_analyzer import analyze_gaps
from app.seed_data import seed_vector_store

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle"""
    logger.info("=" * 50)
    logger.info("Starting Startup Idea Similarity Detector...")
    logger.info("=" * 50)

    # Initialize database
    init_db()
    logger.info("Database initialized.")

    # Load embedding model
    embedder.load_model()

    # Initialize vector store
    vector_store.initialize()

    # Seed data on first run
    seed_vector_store(embedder, vector_store)

    logger.info("Application ready!")
    yield

    # Shutdown
    logger.info("Shutting down...")


app = FastAPI(
    title="Startup Idea Similarity Detector",
    description="Analyze your startup idea and discover similar companies in the market",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
origins = [o.strip() for o in settings.cors_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# Auth Endpoints
# ============================================

@app.post("/api/auth/register", response_model=TokenResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if email already exists
    existing = db.query(User).filter(User.email == request.email.lower().strip()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    user = User(
        id=str(uuid.uuid4()),
        name=request.name.strip(),
        email=request.email.lower().strip(),
        password_hash=hash_password(request.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate token
    token = create_access_token(user.id, user.email, user.name)

    logger.info(f"New user registered: {user.email}")
    return TokenResponse(
        access_token=token,
        user={"id": user.id, "name": user.name, "email": user.email}
    )


@app.post("/api/auth/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login and get access token"""
    user = db.query(User).filter(User.email == request.email.lower().strip()).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user.id, user.email, user.name)

    logger.info(f"User logged in: {user.email}")
    return TokenResponse(
        access_token=token,
        user={"id": user.id, "name": user.name, "email": user.email}
    )


@app.get("/api/auth/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)):
    """Get current user profile"""
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at.isoformat() if user.created_at else None
    )


# ============================================
# History Endpoints
# ============================================

@app.get("/api/history", response_model=HistoryResponse)
async def get_history(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get search history for the authenticated user"""
    searches = db.query(SearchHistory).filter(
        SearchHistory.user_id == user.id
    ).order_by(SearchHistory.created_at.desc()).limit(50).all()

    items = []
    for s in searches:
        items.append(HistoryItem(
            id=s.id,
            input_text=s.input_text,
            uniqueness_score=s.uniqueness_score,
            uniqueness_label=s.uniqueness_label,
            top_matches=s.top_matches,
            gap_analysis=s.gap_analysis,
            created_at=s.created_at.isoformat() if s.created_at else None
        ))

    return HistoryResponse(total=len(items), history=items)


@app.delete("/api/history/{search_id}")
async def delete_history_item(
    search_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a specific search history item"""
    item = db.query(SearchHistory).filter(
        SearchHistory.id == search_id,
        SearchHistory.user_id == user.id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="History item not found")

    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}


# ============================================
# Core Endpoints
# ============================================

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        total_startups=vector_store.get_count(),
        embedding_model=settings.embedding_model,
        version="1.0.0"
    )


@app.get("/api/startups")
async def list_startups():
    """List all startups in the database"""
    from app.seed_data import load_seed_data
    data = load_seed_data()
    return {"total": len(data), "startups": data}


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_idea(
    request: AnalyzeRequest,
    user: User | None = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """Main analysis endpoint - finds similar startups and provides gap analysis"""
    try:
        logger.info(f"Analyzing idea: {request.idea[:100]}...")

        # 1. Generate embedding for user's idea
        query_embedding = embedder.embed(request.idea)

        # 2. Search for similar startups
        raw_results = vector_store.search_similar(query_embedding, top_k=request.top_k)

        # 3. Process and rank results
        matches = process_search_results(raw_results)

        # 4. Compute uniqueness score
        similarity_scores = [m.similarity_score for m in matches]
        uniqueness_score, uniqueness_label = compute_uniqueness_score(similarity_scores)

        # 5. Get category distribution
        category_dist = get_category_distribution(matches)

        # 6. Gap analysis (optional, uses Groq LLM)
        gap_analysis = None
        if request.include_gap_analysis and matches:
            gap_analysis = analyze_gaps(request.idea, matches)

        # 7. Save to search history (linked to user if authenticated)
        search_id = str(uuid.uuid4())
        try:
            history = SearchHistory(
                id=search_id,
                user_id=user.id if user else None,
                input_text=request.idea,
                uniqueness_score=uniqueness_score,
                uniqueness_label=uniqueness_label,
                top_matches=[{
                    "name": m.name,
                    "similarity": m.similarity_percentage
                } for m in matches[:5]],
                gap_analysis=gap_analysis.summary if gap_analysis else None
            )
            db.add(history)
            db.commit()
        except Exception as e:
            logger.error(f"Failed to save search history: {e}")

        # 8. Build response
        return AnalyzeResponse(
            uniqueness_score=uniqueness_score,
            uniqueness_label=uniqueness_label,
            total_comparisons=vector_store.get_count(),
            similar_startups=matches,
            category_distribution=category_dist,
            gap_analysis=gap_analysis,
            search_id=search_id,
            analyzed_at=datetime.utcnow().isoformat()
        )

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
