"""
TakhleeqX Content Writer Agent — Agent 3 in the pipeline.

Generates captions, hashtags, and CTAs for each content pillar
defined by the Strategy Planner.

Demo Talking Point: The Content Writer demonstrates MULTI-OUTPUT GENERATION —
a single agent produces multiple structured artifacts (one post per content
pillar), each ready for downstream visual generation, showing how agents
can scale content production.
"""

import json
import logging
from datetime import datetime, timezone
from openai import OpenAI
from backend.config import get_settings
from backend.agents.state import PipelineState
from backend.prompts.content_prompts import CONTENT_GENERATION_PROMPT

settings = get_settings()
logger = logging.getLogger("takhleeqx.agents.content_writer")


def content_writer_node(state: PipelineState) -> dict:
    """
    LangGraph node function for the Content Writer agent.

    Takes strategy → produces post content for each content pillar.
    """
    logger.info("✍️ Content Writer agent starting...")
    timestamp = datetime.now(timezone.utc).isoformat()

    try:
        strategy = state.get("strategy", {})
        content_pillars = strategy.get("content_pillars", [])

        if not content_pillars:
            raise ValueError("No content pillars found in strategy")

        pillars_text = json.dumps(content_pillars, indent=2)

        # ─── New Frequency Logic ───
        freq = state.get("posting_frequency", "Daily")
        # Default to Daily logic if unknown
        images_count = 5
        reels_count = 2
        total_posts = 7
        
        if freq == "3x/week":
            images_count, reels_count, total_posts = 2, 1, 3
        elif freq == "5x/week" or freq == "Weekdays Only":
            images_count, reels_count, total_posts = 3, 2, 5
        elif freq == "Weekends Only":
            images_count, reels_count, total_posts = 4, 2, 6
            
        post_requirements = f"You MUST generate EXACTLY {total_posts} posts in total.\n"
        post_requirements += f"- EXACTLY {images_count} posts MUST have format: 'image'\n"
        post_requirements += f"- EXACTLY {reels_count} posts MUST have format: 'reel'\n"

        prompt = CONTENT_GENERATION_PROMPT.format(
            campaign_name=strategy.get("campaign_name", "Campaign"),
            target_audience=strategy.get("target_audience", "food lovers"),
            tone=strategy.get("tone", state.get("brand_tone", "fun")),
            visual_style=strategy.get("visual_style", "modern and vibrant"),
            restaurant_name=state["restaurant_name"],
            cuisine_type=state["cuisine_type"],
            target_city=state["target_city"],
            specialties=state.get("specialties", "various dishes"),
            content_pillars=pillars_text,
            post_requirements=post_requirements,
        )

        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
        )

        response_text = response.choices[0].message.content.strip()

        # Parse JSON
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            lines = [l for l in lines[1:] if l.strip() != "```"]
            response_text = "\n".join(lines)

        try:
            content_data = json.loads(response_text)
        except json.JSONDecodeError:
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            content_data = json.loads(response_text[start:end])

        posts = content_data.get("posts", [])
        logger.info(f"✅ Content Writer completed: {len(posts)} posts generated")

        return {
            "posts": posts,
            "current_agent": "visual_designer",
            "agent_logs": [
                {
                    "agent_name": "Content Writer",
                    "status": "done",
                    "message": f"Generated {len(posts)} posts with captions, hashtags, and CTAs.",
                    "timestamp": timestamp,
                }
            ],
        }

    except Exception as e:
        logger.error(f"❌ Content Writer failed: {str(e)}")
        return {
            "posts": [],
            "current_agent": "visual_designer",
            "agent_logs": [
                {
                    "agent_name": "Content Writer",
                    "status": "error",
                    "message": f"Error: {str(e)}",
                    "timestamp": timestamp,
                }
            ],
            "errors": [f"Content Writer: {str(e)}"],
        }
