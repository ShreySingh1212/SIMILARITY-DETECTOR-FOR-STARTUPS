"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# ---- Auth Schemas ----

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    email: str = Field(..., description="User's email address")
    password: str = Field(..., min_length=6, max_length=100, description="Password (min 6 characters)")


class LoginRequest(BaseModel):
    email: str = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict  # {id, name, email}


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: Optional[str] = None


# ---- Request Schemas ----

class AnalyzeRequest(BaseModel):
    idea: str = Field(..., min_length=20, max_length=5000, description="Startup idea description")
    top_k: int = Field(default=10, ge=1, le=20, description="Number of similar startups to return")
    include_gap_analysis: bool = Field(default=True, description="Whether to include AI gap analysis")


# ---- Response Schemas ----

class StartupMatch(BaseModel):
    name: str
    description: str
    category: str
    tags: List[str]
    founded_year: Optional[int] = None
    funding_stage: Optional[str] = None
    status: Optional[str] = None
    url: Optional[str] = None
    similarity_score: float = Field(..., ge=0, le=1)
    similarity_percentage: float = Field(..., ge=0, le=100)


class GapAnalysisResult(BaseModel):
    summary: str
    strengths: List[str]
    weaknesses: List[str]
    differentiators: List[str]
    suggestions: List[str]
    market_saturation: str  # "low", "medium", "high"


class AnalyzeResponse(BaseModel):
    uniqueness_score: float = Field(..., ge=0, le=100)
    uniqueness_label: str  # "Highly Unique", "Moderately Unique", "Crowded Space"
    total_comparisons: int
    similar_startups: List[StartupMatch]
    category_distribution: dict  # {category: count}
    gap_analysis: Optional[GapAnalysisResult] = None
    search_id: str
    analyzed_at: str


class StartupInfo(BaseModel):
    name: str
    description: str
    category: str
    tags: List[str]
    founded_year: Optional[int] = None
    funding_stage: Optional[str] = None
    status: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    total_startups: int
    embedding_model: str
    version: str


# ---- History Schemas ----

class HistoryItem(BaseModel):
    id: str
    input_text: str
    uniqueness_score: Optional[float] = None
    uniqueness_label: Optional[str] = None
    top_matches: Optional[list] = None
    gap_analysis: Optional[str] = None
    created_at: Optional[str] = None


class HistoryResponse(BaseModel):
    total: int
    history: List[HistoryItem]
