"""
TakhleeqX ORM Models — SQLAlchemy models for all database tables.
Tables: users, restaurants, campaigns, posts, trends_cache
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from backend.database import Base


class User(Base):
    """Restaurant owner account for authentication."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)

    # Relationships
    restaurants = relationship("Restaurant", back_populates="owner")


class Restaurant(Base):
    """Restaurant profile — the client entity for campaign generation."""
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(200), nullable=False)
    cuisine_type = Column(String(100), nullable=False)
    target_city = Column(String(100), nullable=False)
    brand_tone = Column(String(100), nullable=False)  # e.g., "fun", "elegant", "bold"
    posting_frequency = Column(String(50), nullable=False)  # e.g., "daily", "3x/week"
    description = Column(Text, nullable=True)
    specialties = Column(Text, nullable=True)  # Comma-separated specialties
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    owner = relationship("User", back_populates="restaurants")
    campaigns = relationship("Campaign", back_populates="restaurant")


class Campaign(Base):
    """Generated marketing campaign — output of the Strategy Planner agent."""
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    campaign_name = Column(String(300), nullable=False)
    target_audience = Column(String(300), nullable=True)
    tone = Column(String(100), nullable=True)
    content_pillars = Column(JSON, nullable=True)  # List of content pillars
    posting_schedule = Column(JSON, nullable=True)  # Schedule details
    trends_data = Column(JSON, nullable=True)  # Raw trends from Trend Scout
    strategy_data = Column(JSON, nullable=True)  # Full strategy JSON
    status = Column(String(50), default="draft")  # draft, approved, published
    quality_score = Column(Integer, nullable=True)  # Supervisor agent score 0-100
    supervisor_notes = Column(Text, nullable=True)  # Supervisor agent assessment
    predicted_analytics = Column(JSON, nullable=True)  # Performance Predictor output
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    restaurant = relationship("Restaurant", back_populates="campaigns")
    posts = relationship("Post", back_populates="campaign")
    agent_logs = relationship("AgentExecutionLog", back_populates="campaign")


class Post(Base):
    """Individual social media post — generated content + image."""
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    caption = Column(Text, nullable=False)
    hashtags = Column(JSON, nullable=True)  # List of hashtags
    cta = Column(String(300), nullable=True)  # Call-to-action
    platform = Column(String(50), default="instagram")
    image_url = Column(Text, nullable=True)  # Path or URL to generated image
    video_url = Column(Text, nullable=True)  # Path or URL to generated reel/video
    alt_text = Column(String(500), nullable=True)
    content_pillar = Column(String(200), nullable=True)
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    campaign = relationship("Campaign", back_populates="posts")


class TrendCache(Base):
    """Cached trend data to avoid repeated API calls."""
    __tablename__ = "trends_cache"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, nullable=True)  # Optional: cache per restaurant
    query_type = Column(String(50), nullable=False)  # "local", "global", or "synthesis"
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AgentExecutionLog(Base):
    """Persistent log of every agent execution — survives server restarts."""
    __tablename__ = "agent_execution_logs"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    agent_name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)  # running, done, error
    message = Column(Text, nullable=True)
    input_summary = Column(Text, nullable=True)  # Brief summary of input data
    output_summary = Column(Text, nullable=True)  # Brief summary of output data
    duration_seconds = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    campaign = relationship("Campaign", back_populates="agent_logs")
