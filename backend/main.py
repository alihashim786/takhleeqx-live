"""
TakhleeqX — FastAPI Application Entry Point.

This is the main application file that:
  - Initializes the database
  - Registers all route modules
  - Configures CORS for the React frontend
  - Serves generated images as static files
  - Sets up logging

Demo Talking Point: The FastAPI backend serves as the API gateway between
the React dashboard and the LangGraph agent pipeline, demonstrating
clean separation of concerns in a production agentic system.
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.config import get_settings
from backend.database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("takhleeqx")

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup/shutdown lifecycle."""
    # Startup
    logger.info("🚀 Initializing TakhleeqX backend...")
    init_db()
    logger.info("✅ Database initialized")

    # Create image output directory
    os.makedirs(settings.IMAGE_OUTPUT_DIR, exist_ok=True)
    logger.info(f"📁 Image directory: {settings.IMAGE_OUTPUT_DIR}")

    yield

    # Shutdown
    logger.info("👋 TakhleeqX backend shutting down")


# ─── Create FastAPI App ────────────────────────────────────────
app = FastAPI(
    title="TakhleeqX API",
    description="AI-Powered Marketing Automation Platform — LangGraph Multi-Agent Pipeline",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# ─── CORS Configuration ───────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Static Files (Generated Images) ──────────────────────────
os.makedirs(settings.IMAGE_OUTPUT_DIR, exist_ok=True)
app.mount("/images", StaticFiles(directory=settings.IMAGE_OUTPUT_DIR), name="images")

# ─── Register Routes ──────────────────────────────────────────
from backend.routes.auth_routes import router as auth_router
from backend.routes.restaurant_routes import router as restaurant_router
from backend.routes.campaign_routes import router as campaign_router
from backend.routes.feed_routes import router as feed_router

app.include_router(auth_router)
app.include_router(restaurant_router)
app.include_router(campaign_router)
app.include_router(feed_router)


# ─── Root Endpoint ─────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "app": "TakhleeqX",
        "version": settings.APP_VERSION,
        "description": "AI-Powered Marketing Automation Platform",
        "docs": "/docs",
        "agents": [
            "Trend Scout",
            "Strategy Planner",
            "Content Writer",
            "Visual Designer",
            "Campaign Publisher",
        ],
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
