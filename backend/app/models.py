"""
SQLAlchemy models for users and search history tracking
"""
from sqlalchemy import Column, String, Float, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationship to search history
    searches = relationship("SearchHistory", back_populates="user", order_by="SearchHistory.created_at.desc()")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    input_text = Column(Text, nullable=False)
    uniqueness_score = Column(Float, nullable=True)
    uniqueness_label = Column(String(50), nullable=True)
    top_matches = Column(JSON, nullable=True)
    gap_analysis = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationship back to user
    user = relationship("User", back_populates="searches")

    def __repr__(self):
        return f"<SearchHistory(id={self.id}, score={self.uniqueness_score})>"
