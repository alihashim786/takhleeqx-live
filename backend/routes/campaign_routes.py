"""
TakhleeqX Campaign Routes — Trigger agent pipeline and retrieve campaign data.
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db, SessionLocal
from backend.models import User, Restaurant, Campaign
from backend.schemas import CampaignResponse, CampaignTrigger
from backend.auth import get_current_user
from backend.agents.graph import run_pipeline

router = APIRouter(prefix="/api/campaigns", tags=["Campaigns"])
logger = logging.getLogger("takhleeqx.routes.campaigns")

# In-memory store for pipeline status (per user session)
pipeline_status_store: dict = {}


def _run_pipeline_background(restaurant_id: int, user_id: int, status_key: str, db_session):
    """Run the agent pipeline in background and update status store."""
    try:
        restaurant = db_session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        if not restaurant:
            pipeline_status_store[status_key] = {
                "status": "failed",
                "error": "Restaurant not found",
                "logs": [],
            }
            return

        # Update status to running
        pipeline_status_store[status_key] = {
            "status": "running",
            "current_agent": "trend_scout",
            "logs": [
                {
                    "agent_name": "Pipeline",
                    "status": "running",
                    "message": "Agent pipeline started",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            ],
        }

        # Build initial state from restaurant profile
        initial_state = {
            "restaurant_id": restaurant.id,
            "restaurant_name": restaurant.name,
            "cuisine_type": restaurant.cuisine_type,
            "target_city": restaurant.target_city,
            "brand_tone": restaurant.brand_tone,
            "posting_frequency": restaurant.posting_frequency,
            "description": restaurant.description or "",
            "specialties": restaurant.specialties or "",
            "user_id": user_id,
        }

        # Run the pipeline
        final_state = run_pipeline(initial_state)

        # Update status store with results
        pipeline_status_store[status_key] = {
            "status": final_state.get("pipeline_status", "completed"),
            "current_agent": "completed",
            "campaign_id": final_state.get("campaign_id"),
            "logs": final_state.get("agent_logs", []),
            "errors": final_state.get("errors", []),
            "trends": {
                "local": final_state.get("local_trends", []),
                "global": final_state.get("global_trends", []),
                "synthesis": final_state.get("trend_synthesis", {}),
            },
            "strategy": final_state.get("strategy", {}),
            "posts": final_state.get("posts", []),
            "posts_count": len(final_state.get("published_posts", [])),
            "quality_score": final_state.get("quality_score"),
            "supervisor_notes": final_state.get("supervisor_notes"),
            "predicted_analytics": final_state.get("predicted_analytics", {}),
        }

        logger.info(f"Pipeline completed for restaurant {restaurant_id}")

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        pipeline_status_store[status_key] = {
            "status": "failed",
            "error": str(e),
            "logs": pipeline_status_store.get(status_key, {}).get("logs", []),
        }
    finally:
        db_session.close()

async def _run_mock_pipeline_background(restaurant_id: int, user_id: int, status_key: str, db_session):
    """Run a simulated pipeline using hardcoded data for demonstration."""
    try:
        import os
        from backend.models import Post
        restaurant = db_session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        r_name = restaurant.name.replace(" ", "_") if restaurant else "KFC"
        base_dir = f"campaign_exports/{r_name}"
        if not os.path.exists(base_dir):
            base_dir = "campaign_exports/KFC"

        def _read_json(filename):
            try:
                with open(os.path.join(base_dir, filename), "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {}
        
        trends_data = _read_json("trends.json")
        strategy_data = _read_json("strategy.json")
        predicted_analytics = _read_json("analytics_prediction.json")
        
        # Parse supervisor review
        try:
            with open(os.path.join(base_dir, "supervisor_review.json"), "r", encoding="utf-8") as f:
                content = f.read()
                try:
                    supervisor_notes = json.loads(content).get("feedback", "Excellent campaign.")
                except:
                    supervisor_notes = content
        except:
            supervisor_notes = "Excellent campaign."

        # Parse posts
        posts_data = _read_json("content_writer_output.json")
        if not isinstance(posts_data, list):
            posts_data = []

        # Create new campaign in DB
        new_campaign = Campaign(
            restaurant_id=restaurant_id,
            campaign_name=strategy_data.get("campaign_name", f"Mock Campaign for {r_name}"),
            target_audience=strategy_data.get("target_audience", ""),
            tone=strategy_data.get("tone", ""),
            content_pillars=strategy_data.get("content_pillars", []),
            posting_schedule=strategy_data.get("posting_schedule", {}),
            trends_data=trends_data,
            strategy_data=strategy_data,
            status="published",
            quality_score=85,
            supervisor_notes=supervisor_notes,
            predicted_analytics=predicted_analytics,
        )
        db_session.add(new_campaign)
        db_session.commit()
        db_session.refresh(new_campaign)

        # Create Posts
        images_dir = os.path.join(base_dir, "images")
        image_files = sorted(os.listdir(images_dir)) if os.path.exists(images_dir) else []
        
        for i, post in enumerate(posts_data):
            image_url = None
            if i < len(image_files):
                image_url = f"/{base_dir}/images/{image_files[i]}"

            db_post = Post(
                campaign_id=new_campaign.id,
                caption=post.get("caption", ""),
                hashtags=post.get("hashtags", []),
                cta=post.get("cta", ""),
                platform="instagram",
                image_url=image_url,
                video_url=None,
                content_pillar=post.get("content_pillar", ""),
                is_published=True,
                published_at=datetime.now(timezone.utc)
            )
            db_session.add(db_post)
        
        db_session.commit()

        logs = [
            {"agent_name": "Pipeline", "status": "running", "message": "Initializing Mock Mode...", "timestamp": datetime.now(timezone.utc).isoformat()},
            {"agent_name": "Trend Scout", "status": "done", "message": "Mock trends identified.", "timestamp": datetime.now(timezone.utc).isoformat()},
            {"agent_name": "Strategy Planner", "status": "done", "message": "Mock strategy generated.", "timestamp": datetime.now(timezone.utc).isoformat()},
            {"agent_name": "Content Writer", "status": "done", "message": "Mock captions generated.", "timestamp": datetime.now(timezone.utc).isoformat()},
            {"agent_name": "Visual Designer", "status": "done", "message": "Mock images created.", "timestamp": datetime.now(timezone.utc).isoformat()},
            {"agent_name": "Reel Producer", "status": "done", "message": "Mock reels rendered.", "timestamp": datetime.now(timezone.utc).isoformat()},
            {"agent_name": "Campaign Publisher", "status": "done", "message": "Campaign published successfully.", "timestamp": datetime.now(timezone.utc).isoformat()}
        ]

        pipeline_status_store[status_key] = {
            "status": "completed",
            "current_agent": "completed",
            "campaign_id": new_campaign.id,
            "logs": logs,
        }
    except Exception as e:
        logger.error(f"Mock pipeline failed: {str(e)}")
        pipeline_status_store[status_key] = {
            "status": "failed", 
            "error": str(e),
            "logs": [{"agent_name": "Pipeline", "status": "failed", "message": f"Error: {str(e)}", "timestamp": datetime.now(timezone.utc).isoformat()}]
        }
    finally:
        db_session.close()


from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Request

@router.post("/trigger")
def trigger_pipeline(
    request: Request,
    payload: CampaignTrigger,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Trigger the full agent pipeline for a restaurant."""
    # Verify restaurant ownership
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == payload.restaurant_id, Restaurant.owner_id == current_user.id)
        .first()
    )
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    status_key = f"{current_user.id}_{payload.restaurant_id}"

    # Check if already running
    current = pipeline_status_store.get(status_key, {})
    if current.get("status") == "running":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Pipeline already running for this restaurant",
        )

    # Check for API Key in headers
    openai_key = request.headers.get("x-openai-key")

    new_db = SessionLocal()
    if openai_key and openai_key.startswith("sk-"):
        # Live mode: update state or environment for this run
        import os
        os.environ["OPENAI_API_KEY"] = openai_key
        background_tasks.add_task(
            _run_pipeline_background,
            payload.restaurant_id,
            current_user.id,
            status_key,
            new_db,
        )
    else:
        # Mock mode
        background_tasks.add_task(
            _run_mock_pipeline_background,
            payload.restaurant_id,
            current_user.id,
            status_key,
            new_db,
        )

    return {"message": "Pipeline started", "status_key": status_key, "mode": "live" if openai_key else "mock"}


@router.get("/status/{restaurant_id}")
def get_pipeline_status(
    restaurant_id: int,
    current_user: User = Depends(get_current_user),
):
    """Get current pipeline status for a restaurant."""
    status_key = f"{current_user.id}_{restaurant_id}"
    status_data = pipeline_status_store.get(status_key)

    if not status_data:
        return {"status": "idle", "logs": []}

    return status_data


@router.get("/stream/{restaurant_id}")
async def stream_pipeline_status(
    restaurant_id: int,
    current_user: User = Depends(get_current_user),
):
    """SSE endpoint for real-time pipeline status updates."""
    status_key = f"{current_user.id}_{restaurant_id}"

    async def event_generator():
        last_log_count = 0
        while True:
            status_data = pipeline_status_store.get(status_key, {"status": "idle"})

            # Send update
            yield f"data: {json.dumps(status_data)}\n\n"

            # Stop streaming if pipeline is done or failed
            if status_data.get("status") in ("completed", "failed"):
                break

            await asyncio.sleep(2)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/", response_model=List[CampaignResponse])
def list_campaigns(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all campaigns for the current user's restaurants."""
    restaurant_ids = [
        r.id
        for r in db.query(Restaurant).filter(Restaurant.owner_id == current_user.id).all()
    ]
    if not restaurant_ids:
        return []

    return (
        db.query(Campaign)
        .filter(Campaign.restaurant_id.in_(restaurant_ids))
        .order_by(Campaign.created_at.desc())
        .all()
    )


@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific campaign by ID."""
    restaurant_ids = [
        r.id
        for r in db.query(Restaurant).filter(Restaurant.owner_id == current_user.id).all()
    ]
    campaign = (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id, Campaign.restaurant_id.in_(restaurant_ids))
        .first()
    )
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign
