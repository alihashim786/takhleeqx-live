"""
TakhleeqX Campaign Publisher Agent — Agent 5 in the pipeline.

Assembles final posts (caption + image + hashtags) and persists them
to the database, making them visible in the simulated social feed.

Demo Talking Point: The Campaign Publisher demonstrates the PERSISTENCE LAYER
of the agentic system — it writes the final assembled outputs to the database,
completing the pipeline and making content available via the REST API, simulating
what a real social media posting API would do.
"""

import os
import json
import shutil
import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import Campaign, Post
from backend.agents.state import PipelineState

logger = logging.getLogger("takhleeqx.agents.campaign_publisher")


def campaign_publisher_node(state: PipelineState) -> dict:
    """
    LangGraph node function for the Campaign Publisher agent.

    Assembles posts with images and saves to database.
    """
    logger.info("📤 Campaign Publisher agent starting...")
    timestamp = datetime.now(timezone.utc).isoformat()

    db: Session = SessionLocal()
    try:
        strategy = state.get("strategy", {})
        posts = state.get("posts", [])
        visuals = state.get("visuals", [])

        # Create or update campaign in DB
        campaign = Campaign(
            restaurant_id=state["restaurant_id"],
            campaign_name=strategy.get("campaign_name", "Untitled Campaign"),
            target_audience=strategy.get("target_audience", ""),
            tone=strategy.get("tone", ""),
            content_pillars=strategy.get("content_pillars", []),
            posting_schedule=strategy.get("posting_schedule", {}),
            trends_data={
                "local_trends": state.get("local_trends", []),
                "global_trends": state.get("global_trends", []),
                "synthesis": state.get("trend_synthesis", {}),
            },
            strategy_data=strategy,
            status="published",
        )
        db.add(campaign)
        db.flush()  # Get campaign ID

        # Build visual lookup by post_id
        visual_map = {}
        for v in visuals:
            pid = v.get("post_id")
            if pid is not None:
                visual_map[pid] = v

        from datetime import timedelta
        
        freq = state.get("posting_frequency", "Daily")
        base_time = datetime.now(timezone.utc)
        
        # Calculate next Saturday for Weekends logic
        days_ahead_sat = 5 - base_time.weekday()
        if days_ahead_sat <= 0:
            days_ahead_sat += 7
        next_sat = base_time + timedelta(days=days_ahead_sat)
        next_sun = next_sat + timedelta(days=1)
        
        # Schedule posts in DB
        published_posts = []
        for i, post in enumerate(posts):
            post_id = post.get("post_id", 0)
            visual = visual_map.get(post_id, {})
            
            # Determine scheduled time
            scheduled_time = base_time
            if freq == "Daily":
                scheduled_time = base_time + timedelta(days=i)
            elif freq == "3x/week":
                # Monday, Wednesday, Friday (just stagger by 2 days starting tomorrow)
                scheduled_time = base_time + timedelta(days=1 + (i*2))
            elif freq == "5x/week" or freq == "Weekdays Only":
                # Stagger across 5 days
                scheduled_time = base_time + timedelta(days=1 + i)
            elif freq == "Weekends Only":
                # 3 on Saturday, 3 on Sunday
                is_sunday = i >= 3
                day_base = next_sun if is_sunday else next_sat
                hours_offset = [10, 14, 18] # 10 AM, 2 PM, 6 PM
                hour = hours_offset[i % 3]
                scheduled_time = day_base.replace(hour=hour, minute=0, second=0, microsecond=0)
            else:
                scheduled_time = base_time + timedelta(days=i)
                
            # Formatting for UI friendly
            time_str = scheduled_time.strftime("%A, %I:%M %p")

            db_post = Post(
                campaign_id=campaign.id,
                caption=post.get("caption", ""),
                hashtags=post.get("hashtags", []),
                cta=post.get("cta", ""),
                platform=post.get("platform", "Instagram"),
                image_url=visual.get("image_url") or post.get("image_url"),
                video_url=post.get("video_url"),
                alt_text=visual.get("alt_text", ""),
                content_pillar=post.get("content_pillar", ""),
                is_published=True,
                published_at=scheduled_time,
            )
            db.add(db_post)
            db.flush()

            published_posts.append({
                "db_id": db_post.id,
                "post_id": post_id,
                "caption": post.get("caption", ""),
                "hashtags": post.get("hashtags", []),
                "image_url": visual.get("image_url") or post.get("image_url"),
                "video_url": post.get("video_url"),
                "platform": post.get("platform", "Instagram"),
                "scheduled_time_str": time_str,
                "published_at": scheduled_time.isoformat(),
            })

        # Update the campaign's posting_schedule with the exact scheduled times
        if not campaign.posting_schedule:
            campaign.posting_schedule = {}
        schedule_copy = dict(campaign.posting_schedule)
        schedule_copy["frequency"] = freq
        schedule_copy["best_times"] = [p["scheduled_time_str"] for p in published_posts]
        campaign.posting_schedule = schedule_copy

        db.commit()
        logger.info(f"✅ Campaign Publisher completed: {len(published_posts)} posts published to DB")

        # ─── Save campaign data locally for demo ───────────────────
        _export_campaign_locally(state, campaign, published_posts)

        return {
            "campaign_id": campaign.id,
            "published_posts": published_posts,
            "current_agent": "completed",
            "pipeline_status": "completed",
            "agent_logs": [
                {
                    "agent_name": "Campaign Publisher",
                    "status": "done",
                    "message": f"Published {len(published_posts)} posts to campaign '{campaign.campaign_name}'.",
                    "timestamp": timestamp,
                }
            ],
        }

    except Exception as e:
        db.rollback()
        logger.error(f"❌ Campaign Publisher failed: {str(e)}")
        return {
            "published_posts": [],
            "current_agent": "completed",
            "pipeline_status": "failed",
            "agent_logs": [
                {
                    "agent_name": "Campaign Publisher",
                    "status": "error",
                    "message": f"Error: {str(e)}",
                    "timestamp": timestamp,
                }
            ],
            "errors": [f"Campaign Publisher: {str(e)}"],
        }
    finally:
        db.close()


def _export_campaign_locally(state: dict, campaign, published_posts: list):
    """Save the last campaign data to project directory for demo showcase."""
    try:
        restaurant_name = state.get("restaurant_name", "Unknown").replace(" ", "_")
        export_dir = os.path.join("campaign_exports", restaurant_name)
        os.makedirs(export_dir, exist_ok=True)

        # 1. Trends
        with open(os.path.join(export_dir, "trends.json"), "w", encoding="utf-8") as f:
            json.dump({
                "local_trends": state.get("local_trends", []),
                "global_trends": state.get("global_trends", []),
                "synthesis": state.get("trend_synthesis", {}),
            }, f, indent=2, ensure_ascii=False)

        # 2. Strategy summary
        with open(os.path.join(export_dir, "strategy.json"), "w", encoding="utf-8") as f:
            json.dump(state.get("strategy", {}), f, indent=2, ensure_ascii=False)

        # 3. Content Writer output
        posts_export = []
        for p in state.get("posts", []):
            posts_export.append({
                "post_id": p.get("post_id"),
                "caption": p.get("caption"),
                "hashtags": p.get("hashtags"),
                "cta": p.get("cta"),
                "content_pillar": p.get("content_pillar"),
            })
        with open(os.path.join(export_dir, "content_writer_output.json"), "w", encoding="utf-8") as f:
            json.dump(posts_export, f, indent=2, ensure_ascii=False)

        # 4. Copy generated images
        images_dir = os.path.join(export_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        for v in state.get("visuals", []):
            fn = v.get("filename")
            if fn:
                src = os.path.join("generated_images", fn)
                if os.path.exists(src):
                    shutil.copy2(src, os.path.join(images_dir, fn))

        # 5. Save first reel URL
        reels = state.get("reels", [])
        with open(os.path.join(export_dir, "reels.json"), "w", encoding="utf-8") as f:
            json.dump(reels[:1] if reels else [], f, indent=2, ensure_ascii=False)

        # 6. Supervisor review
        with open(os.path.join(export_dir, "supervisor_review.json"), "w", encoding="utf-8") as f:
            json.dump({
                "quality_score": state.get("quality_score"),
                "supervisor_notes": state.get("supervisor_notes"),
                "agent_evaluations": state.get("agent_evaluations"),
            }, f, indent=2, ensure_ascii=False)

        # 7. Analytics summary
        with open(os.path.join(export_dir, "analytics_prediction.json"), "w", encoding="utf-8") as f:
            json.dump(state.get("predicted_analytics", {}), f, indent=2, ensure_ascii=False)

        logger.info(f"📂 Campaign data exported to: {export_dir}")

    except Exception as e:
        logger.warning(f"⚠️ Local export failed (non-critical): {e}")
