"""
TakhleeqX Reel Producer Agent — Agent 5 in the pipeline.

Takes the outputs from Visual Designer (images) and Content Writer (text),
uses GPT-4o to write a Pakistani meme script, and sends it to Creatomate
to generate a Reel/TikTok video.
"""

import os
import json
import logging
import httpx
from datetime import datetime, timezone
from openai import OpenAI
from backend.config import get_settings
from backend.agents.state import PipelineState
from backend.prompts.reel_prompts import REEL_SCRIPT_PROMPT

settings = get_settings()
logger = logging.getLogger("takhleeqx.agents.reel_producer")

def _generate_script(prompt: str) -> dict:
    api_key = os.environ.get("OPENAI_API_KEY", settings.OPENAI_API_KEY)
    client = OpenAI(api_key=api_key)
    try:
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
            
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        return json.loads(response_text[start:end])
    except Exception as e:
        logger.error(f"Script generation failed: {e}")
        return {
            "voiceover_script": "This food is amazing, you have to try it!",
            "on_screen_text": "Yum!",
            "scene_description": "Delicious food"
        }

def _generate_creatomate_video(script_data: dict, image_url: str) -> str:
    # A fun fallback meme video URL to use if Creatomate is not configured or fails
    fallback_video = "https://f002.backblazeb2.com/file/creatomate-c8xg3hsxdu/31dd2e29-808d-4843-a5a3-f416851f3b0a.mp4"
    
    if not settings.CREATOMATE_API_KEY or not settings.CREATOMATE_TEMPLATE_ID:
        logger.warning("Creatomate API Key or Template ID missing. Using fallback video.")
        return fallback_video

    try:
        modifications = {
            "Background-Image": image_url,
            # We assume the user renames these text elements in the Creatomate editor
            "Shahbaz-Text-1": script_data.get("shahbaz_msg_1", ""),
            "Trump-Text-1": script_data.get("trump_msg_1", ""),
            "Shahbaz-Text-2": script_data.get("shahbaz_msg_2", ""),
            "Brand-Name": script_data.get("brand_name", ""),
            "Tagline": script_data.get("tagline", "")
        }

        payload = {
            "template_id": settings.CREATOMATE_TEMPLATE_ID,
            "modifications": modifications
        }

        headers = {
            "Authorization": f"Bearer {settings.CREATOMATE_API_KEY}",
            "Content-Type": "application/json"
        }

        # We request a synchronous render for simplicity, or grab the render URL
        # We will grab the URL to the video stream / status
        response = httpx.post(
            "https://api.creatomate.com/v1/renders",
            json=payload,
            headers=headers,
            timeout=30.0
        )
        response.raise_for_status()
        data = response.json()
        
        # 'data' contains the render info. The URL will be available at data[0]['url']
        # But rendering takes time, so we return the URL where it WILL be available.
        if isinstance(data, list) and len(data) > 0:
            return data[0].get("url")
        return data.get("url")
        
    except Exception as e:
        logger.error(f"Creatomate API failed: {e}. Using fallback video.")
        return fallback_video

def reel_producer_node(state: PipelineState) -> dict:
    """
    LangGraph node function for the Reel Producer agent.
    """
    logger.info("🎬 Reel Producer agent starting...")
    timestamp = datetime.now(timezone.utc).isoformat()

    try:
        posts = state.get("posts", [])
        visuals = state.get("visuals", [])
        reels = []

        if not posts:
            raise ValueError("No posts found to generate reels for")

        # Varied high-quality food backgrounds for Creatomate (it can't access localhost)
        unsplash_backgrounds = [
            "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=1024",
            "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=1024",
            "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=1024",
            "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1024",
            "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=1024",
            "https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?w=1024",
        ]

        for i, post in enumerate(posts):
            post_id = post.get("post_id", i + 1)
            
            if post.get("format") == "image":
                logger.info(f"Skipping Reel Producer for post {post_id} (format is image)")
                reels.append({})
                continue

            # Always use Unsplash for variety on reels since AI images are used for image posts
            image_url = unsplash_backgrounds[i % len(unsplash_backgrounds)]

            # 1. Generate Script
            script_prompt = REEL_SCRIPT_PROMPT.format(
                restaurant_name=state["restaurant_name"],
                cuisine_type=state["cuisine_type"],
                target_city=state["target_city"],
                brand_tone=state["brand_tone"],
                caption_summary=post.get("caption", "")[:200]
            )
            
            logger.info(f"Generating script for post {post_id}...")
            script_data = _generate_script(script_prompt)

            # 2. Generate Video via Creatomate
            logger.info(f"Triggering Creatomate for post {post_id}...")
            video_url = _generate_creatomate_video(script_data, image_url)
            
            reels.append({
                "post_id": post_id,
                "script_data": script_data,
                "video_url": video_url
            })
            
            # Attach the video URL back to the posts array so campaign_publisher can save it
            if video_url:
                post["video_url"] = video_url

        logger.info(f"✅ Reel Producer completed: {len(reels)} reels generated")

        return {
            "posts": posts, # updated with video_url
            "reels": reels,
            "current_agent": "campaign_publisher",
            "agent_logs": [
                {
                    "agent_name": "Reel Producer",
                    "status": "done",
                    "message": f"Generated scripts and triggered {len(reels)} reels using Creatomate.",
                    "timestamp": timestamp,
                }
            ],
        }

    except Exception as e:
        logger.error(f"❌ Reel Producer failed: {str(e)}")
        return {
            "reels": [],
            "current_agent": "campaign_publisher",
            "agent_logs": [
                {
                    "agent_name": "Reel Producer",
                    "status": "error",
                    "message": f"Error: {str(e)}",
                    "timestamp": timestamp,
                }
            ],
            "errors": [f"Reel Producer: {str(e)}"],
        }
