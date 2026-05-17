"""
TakhleeqX Pydantic Schemas — Request/response models for API validation.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ─── Auth Schemas ───────────────────────────────────────────────
class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Restaurant Schemas ────────────────────────────────────────
class RestaurantCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    cuisine_type: str = Field(min_length=2, max_length=100)
    target_city: str = Field(min_length=2, max_length=100)
    brand_tone: str = Field(min_length=2, max_length=100)
    posting_frequency: str = Field(min_length=2, max_length=50)
    description: Optional[str] = None
    specialties: Optional[str] = None


class RestaurantResponse(BaseModel):
    id: int
    owner_id: int
    name: str
    cuisine_type: str
    target_city: str
    brand_tone: str
    posting_frequency: str
    description: Optional[str]
    specialties: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Campaign Schemas ──────────────────────────────────────────
class CampaignResponse(BaseModel):
    id: int
    restaurant_id: int
    campaign_name: str
    target_audience: Optional[str]
    tone: Optional[str]
    content_pillars: Optional[list]
    posting_schedule: Optional[dict]
    trends_data: Optional[dict]
    strategy_data: Optional[dict]
    status: str
    quality_score: Optional[int] = None
    supervisor_notes: Optional[str] = None
    predicted_analytics: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CampaignTrigger(BaseModel):
    restaurant_id: int


# ─── Post Schemas ──────────────────────────────────────────────
class PostResponse(BaseModel):
    id: int
    campaign_id: int
    caption: str
    hashtags: Optional[list]
    cta: Optional[str]
    platform: str
    image_url: Optional[str]
    video_url: Optional[str] = None
    alt_text: Optional[str]
    content_pillar: Optional[str]
    is_published: bool
    published_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Agent Status Schemas ──────────────────────────────────────
class AgentStatus(BaseModel):
    agent_name: str
    status: str  # idle, running, done, error
    message: Optional[str] = None
    output: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.now)
