"""
TakhleeqX Feed Routes — Endpoints for the simulated social media feed.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import User, Restaurant, Campaign, Post
from backend.schemas import PostResponse
from backend.auth import get_current_user

router = APIRouter(prefix="/api/feed", tags=["Social Feed"])


@router.get("/", response_model=List[PostResponse])
def get_feed(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all published posts for the social feed view."""
    restaurant_ids = [
        r.id
        for r in db.query(Restaurant).filter(Restaurant.owner_id == current_user.id).all()
    ]
    if not restaurant_ids:
        return []

    campaign_ids = [
        c.id
        for c in db.query(Campaign).filter(Campaign.restaurant_id.in_(restaurant_ids)).all()
    ]
    if not campaign_ids:
        return []

    return (
        db.query(Post)
        .filter(Post.campaign_id.in_(campaign_ids), Post.is_published == True)
        .order_by(Post.published_at.desc())
        .all()
    )


@router.get("/campaign/{campaign_id}", response_model=List[PostResponse])
def get_campaign_posts(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all posts for a specific campaign."""
    return (
        db.query(Post)
        .filter(Post.campaign_id == campaign_id)
        .order_by(Post.created_at.asc())
        .all()
    )
