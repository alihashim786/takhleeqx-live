"""
TakhleeqX Database — SQLAlchemy engine, session management, and base model.
Uses SQLite for local development with async-compatible session factory.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.config import get_settings

settings = get_settings()

# SQLite requires check_same_thread=False for FastAPI's threaded model
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables. Called on application startup."""
    from backend.models import User, Restaurant, Campaign, Post, TrendCache, AgentExecutionLog  # noqa: F401
    Base.metadata.create_all(bind=engine)
