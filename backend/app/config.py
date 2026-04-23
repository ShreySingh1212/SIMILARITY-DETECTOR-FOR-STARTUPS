"""
Application configuration - reads from .env file
"""
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # API Keys
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")
    huggingface_api_key: str = os.getenv("HUGGINGFACE_API_KEY", "")
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", "")

    # App Settings
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")
    chroma_db_path: str = os.getenv("CHROMA_DB_PATH", "./data/chroma_db")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://localhost:5173")

    # JWT Auth
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "default_secret_change_me")
    jwt_expiry_hours: int = int(os.getenv("JWT_EXPIRY_HOURS", "24"))

    class Config:
        env_file = ".env"


settings = Settings()
