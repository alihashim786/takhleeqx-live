"""
TakhleeqX Auth Routes — JWT-based registration and login endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
import httpx
import os
import logging
from backend.database import get_db
from backend.models import User
from backend.schemas import UserRegister, UserLogin, TokenResponse, UserResponse
from backend.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
logger = logging.getLogger("takhleeqx.routes.auth")

def send_notification_email(subject: str, message: str):
    """Send an email notification using Resend API to the admin."""
    resend_key = os.environ.get("RESEND_API_KEY")
    if not resend_key:
        logger.warning("No RESEND_API_KEY found. Skipping notification.")
        return
        
    try:
        # For free tier, Resend requires from: onboarding@resend.dev
        # and to: the verified email of the account owner.
        admin_email = os.environ.get("ADMIN_EMAIL", "syedalihashim14@gmail.com") 
        data = {
            "from": "onboarding@resend.dev",
            "to": [admin_email],
            "subject": subject,
            "html": f"<p>{message}</p>"
        }
        headers = {
            "Authorization": f"Bearer {resend_key}",
            "Content-Type": "application/json"
        }
        with httpx.Client() as client:
            client.post("https://api.resend.com/emails", json=data, headers=headers)
    except Exception as e:
        logger.error(f"Failed to send email notification: {e}")

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Register a new restaurant owner account."""
    # Check if email already exists
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    # Check if username already exists
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    # Create user
    user = User(
        email=payload.email,
        username=payload.username,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    background_tasks.add_task(
        send_notification_email, 
        "TakhleeqX: New User Registered", 
        f"A new user has registered:<br/>Username: {user.username}<br/>Email: {user.email}<br/>Name: {user.full_name}"
    )

    # Generate token
    token = create_access_token({"user_id": user.id, "username": user.username})

    return TokenResponse(
        access_token=token,
        user_id=user.id,
        username=user.username,
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Login with username and password."""
    user = db.query(User).filter(User.username == payload.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist. Please register first.",
        )
    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password. Please try again.",
        )

    background_tasks.add_task(
        send_notification_email, 
        "TakhleeqX: User Logged In", 
        f"User logged in:<br/>Username: {user.username}"
    )

    token = create_access_token({"user_id": user.id, "username": user.username})

    return TokenResponse(
        access_token=token,
        user_id=user.id,
        username=user.username,
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user profile."""
    return current_user
