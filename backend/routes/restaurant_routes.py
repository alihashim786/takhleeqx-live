"""
TakhleeqX Restaurant Routes — CRUD for restaurant profiles.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import User, Restaurant
from backend.schemas import RestaurantCreate, RestaurantResponse
from backend.auth import get_current_user

router = APIRouter(prefix="/api/restaurants", tags=["Restaurants"])


@router.post("/", response_model=RestaurantResponse, status_code=status.HTTP_201_CREATED)
def create_restaurant(
    payload: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Onboard a new restaurant profile."""
    restaurant = Restaurant(
        owner_id=current_user.id,
        name=payload.name,
        cuisine_type=payload.cuisine_type,
        target_city=payload.target_city,
        brand_tone=payload.brand_tone,
        posting_frequency=payload.posting_frequency,
        description=payload.description,
        specialties=payload.specialties,
    )
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant


@router.get("/", response_model=List[RestaurantResponse])
def list_restaurants(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all restaurants owned by the current user."""
    return db.query(Restaurant).filter(Restaurant.owner_id == current_user.id).all()


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific restaurant by ID."""
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id, Restaurant.owner_id == current_user.id)
        .first()
    )
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant
