"""
TakhleeqX Performance Predictor Agent — Agent 7 in the pipeline.

Uses GPT-4o to predict engagement metrics for the generated campaign
based on content quality, trend alignment, and platform benchmarks.

Demo Talking Point: Since we're not posting to real social media yet,
the Performance Predictor uses AI to ESTIMATE engagement metrics —
reach, impressions, engagement rate, and best posting times — based
on the generated content quality, hashtag relevance, and Pakistani
food industry benchmarks. This demonstrates PREDICTIVE ANALYTICS
as an agent capability.
"""

import json
import logging
from datetime import datetime, timezone
from openai import OpenAI
from backend.config import get_settings
from backend.agents.state import PipelineState
from backend.database import SessionLocal
from backend.models import Campaign

settings = get_settings()
logger = logging.getLogger("takhleeqx.agents.performance_predictor")

PREDICTOR_PROMPT = """You are a Social Media Performance Predictor for Pakistani restaurants.

Based on the campaign details below, predict realistic engagement metrics for 
a restaurant Instagram/Facebook page with ~5,000-15,000 followers in Pakistan.

## Campaign Details
- Restaurant: {restaurant_name} ({cuisine_type}) in {target_city}
- Campaign Name: {campaign_name}
- Tone: {brand_tone}
- Number of Posts: {post_count}
- Quality Score: {quality_score}/100
- Content Pillars: {content_pillars}
- Sample Hashtags: {sample_hashtags}

## Predict metrics for the first WEEK of this campaign:

Respond with ONLY this JSON:
{{
    "predicted_reach": <integer, realistic for Pakistani food account>,
    "predicted_impressions": <integer>,
    "predicted_engagement_rate": <float, 2 decimals, e.g. 5.2>,
    "predicted_profile_visits": <integer>,
    "predicted_saves": <integer>,
    "predicted_shares": <integer>,
    "best_posting_times": ["<time1>", "<time2>", "<time3>"],
    "top_performing_pillar": "<name of content pillar likely to perform best>",
    "platform_breakdown": {{
        "instagram": {{
            "reach": <integer>,
            "engagement": <float>
        }},
        "facebook": {{
            "reach": <integer>,
            "engagement": <float>
        }}
    }},
    "weekly_growth_prediction": {{
        "followers_gained": <integer>,
        "engagement_trend": "<increasing/stable/decreasing>",
        "viral_potential": "<low/medium/high>"
    }},
    "recommendations": [
        "<actionable recommendation 1>",
        "<actionable recommendation 2>",
        "<actionable recommendation 3>"
    ]
}}
"""


def _parse_json_safe(text: str) -> dict:
    """Extract JSON from LLM response."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        lines = [l for l in lines[1:] if l.strip() != "```"]
        cleaned = "\n".join(lines)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        if start != -1 and end > start:
            try:
                return json.loads(cleaned[start:end])
            except json.JSONDecodeError:
                pass
        return {"error": "Failed to parse prediction"}


def performance_predictor_node(state: PipelineState) -> dict:
    """
    LangGraph node for the Performance Predictor agent.
    
    Predicts engagement metrics based on campaign content and quality.
    """
    logger.info("📊 Performance Predictor agent starting...")
    timestamp = datetime.now(timezone.utc).isoformat()

    db = SessionLocal()
    try:
        strategy = state.get("strategy", {})
        posts = state.get("posts", [])
        quality_score = state.get("quality_score", 75)

        # Gather sample hashtags from posts
        all_hashtags = []
        for p in posts:
            all_hashtags.extend(p.get("hashtags", [])[:3])
        sample_hashtags = ", ".join(all_hashtags[:8]) if all_hashtags else "N/A"

        prompt = PREDICTOR_PROMPT.format(
            restaurant_name=state["restaurant_name"],
            cuisine_type=state["cuisine_type"],
            target_city=state["target_city"],
            campaign_name=strategy.get("campaign_name", "N/A"),
            brand_tone=state["brand_tone"],
            post_count=len(posts),
            quality_score=quality_score or 75,
            content_pillars=json.dumps(strategy.get("content_pillars", []))[:200],
            sample_hashtags=sample_hashtags,
        )

        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
        predictions = _parse_json_safe(response.choices[0].message.content)

        # ─── Save predictions to campaign in DB ────────────────
        campaign_id = state.get("campaign_id")
        if campaign_id:
            campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
            if campaign:
                campaign.predicted_analytics = predictions
                db.commit()

        logger.info(f"✅ Performance Predictor completed — Predicted reach: {predictions.get('predicted_reach', 'N/A')}")

        return {
            "predicted_analytics": predictions,
            "current_agent": "completed",
            "pipeline_status": "completed",
            "agent_logs": [
                {
                    "agent_name": "Performance Predictor",
                    "status": "done",
                    "message": f"Predicted reach: {predictions.get('predicted_reach', 'N/A')}, engagement rate: {predictions.get('predicted_engagement_rate', 'N/A')}%",
                    "timestamp": timestamp,
                }
            ],
        }

    except Exception as e:
        logger.error(f"❌ Performance Predictor failed: {str(e)}")
        return {
            "predicted_analytics": {},
            "current_agent": "completed",
            "pipeline_status": "completed",  # Don't fail the whole pipeline for predictions
            "agent_logs": [
                {
                    "agent_name": "Performance Predictor",
                    "status": "error",
                    "message": f"Error: {str(e)}",
                    "timestamp": timestamp,
                }
            ],
            "errors": [f"Performance Predictor: {str(e)}"],
        }
    finally:
        db.close()
