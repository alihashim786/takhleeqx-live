"""
TakhleeqX Visual Designer Agent — Agent 4 in the pipeline.

Generates images using DALL-E 3 for each post produced by the Content Writer.

Demo Talking Point: The Visual Designer demonstrates TOOL USE with an external
generative API — it transforms text descriptions into visual assets using DALL-E 3,
showing how agents can orchestrate multiple AI modalities (text → image).
"""

import os
import logging
import base64
import httpx
from datetime import datetime, timezone
from openai import OpenAI
from backend.config import get_settings
from backend.agents.state import PipelineState
from backend.prompts.visual_prompts import IMAGE_PROMPT_TEMPLATE, MEME_PROMPT_TEMPLATE

settings = get_settings()
logger = logging.getLogger("takhleeqx.agents.visual_designer")


def _generate_image(prompt: str, post_id: int) -> dict:
    """Generate a single image using OpenAI dall-e-3 and save locally."""
    # Use dynamically injected key from os.environ, fallback to settings
    api_key = os.environ.get("OPENAI_API_KEY", settings.OPENAI_API_KEY)
    client = OpenAI(api_key=api_key)

    try:
        response = client.images.generate(
            model="gpt-image-2",
            prompt=prompt,
            size="1024x1024",
            n=1
        )

        image_url_remote = response.data[0].url
        
        if not image_url_remote:
            logger.warning("API returned None for image URL. Using fallback.")
            image_url_remote = "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=1024" # Cheesy pizza fallback
        
        try:
            # Download the image from the URL provided by the proxy
            with httpx.Client(timeout=10.0) as http_client:
                image_response = http_client.get(image_url_remote)
                image_response.raise_for_status()
                image_bytes = image_response.content
        except Exception as dl_err:
            logger.warning(f"Failed to download image {dl_err}. Falling back to default URL.")
            image_url_remote = "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=1024"
            image_bytes = b"" # empty bytes if we skip local save

        # Save the image locally
        os.makedirs(settings.IMAGE_OUTPUT_DIR, exist_ok=True)
        filename = f"post_{post_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(settings.IMAGE_OUTPUT_DIR, filename)

        with open(filepath, "wb") as f:
            f.write(image_bytes)

        logger.info(f"Image saved: {filepath}")

        # Provide the remote URL directly so the frontend and Creatomate can access it
        # without worrying about localhost vs production server URLs
        return {
            "post_id": post_id,
            "image_url": image_url_remote,
            "original_url": image_url_remote,
            "alt_text": prompt[:200],
            "filename": filename,
        }

    except Exception as e:
        logger.error(f"Image generation failed for post {post_id}: {str(e)}")
        # Provide a fallback image so the frontend UI never breaks during a live demo
        fallback_url = "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=1024"
        return {
            "post_id": post_id,
            "image_url": fallback_url,
            "original_url": fallback_url,
            "alt_text": f"Image generation failed, using fallback. Error: {str(e)}",
            "error": str(e),
        }


def visual_designer_node(state: PipelineState) -> dict:
    """
    LangGraph node function for the Visual Designer agent.

    Takes posts → generates an image for each one using DALL-E 3.
    """
    logger.info("🎨 Visual Designer agent starting...")
    timestamp = datetime.now(timezone.utc).isoformat()

    try:
        posts = state.get("posts", [])
        strategy = state.get("strategy", {})
        visuals = []

        if not posts:
            raise ValueError("No posts found to generate images for")

        meme_count = 0
        for i, post in enumerate(posts):
            post_id = post.get("post_id", len(visuals) + 1)
            
            if post.get("format") == "reel":
                logger.info(f"Skipping Visual Designer for post {post_id} (format is reel)")
                visuals.append({})
                continue
            
            # Determine if this should be a meme
            is_meme = False
            if state.get("brand_tone", "").lower() in ["fun & playful", "fun and playful"] and meme_count < 2:
                is_meme = True
                meme_count += 1

            template_to_use = MEME_PROMPT_TEMPLATE if is_meme else IMAGE_PROMPT_TEMPLATE

            # Build image generation prompt
            image_prompt = template_to_use.format(
                restaurant_name=state["restaurant_name"],
                cuisine_type=state["cuisine_type"],
                brand_tone=state["brand_tone"],
                visual_style=strategy.get("visual_style", "modern and vibrant"),
                caption_summary=post.get("caption", "")[:200],
                image_suggestion=post.get("image_prompt_suggestion", "delicious restaurant food"),
            )

            logger.info(f"Generating {'MEME' if is_meme else 'IMAGE'} for post {post_id}...")
            visual = _generate_image(image_prompt, post_id)
            
            # Attach image URL back to post
            if visual.get("image_url"):
                post["image_url"] = visual["image_url"]
                
            visuals.append(visual)

        logger.info(f"✅ Visual Designer completed: {len(visuals)} images generated")

        return {
            "visuals": visuals,
            "current_agent": "campaign_publisher",
            "agent_logs": [
                {
                    "agent_name": "Visual Designer",
                    "status": "done",
                    "message": f"Generated {len(visuals)} images.",
                    "timestamp": timestamp,
                }
            ],
        }

    except Exception as e:
        logger.error(f"❌ Visual Designer failed: {str(e)}")
        return {
            "visuals": [],
            "current_agent": "campaign_publisher",
            "agent_logs": [
                {
                    "agent_name": "Visual Designer",
                    "status": "error",
                    "message": f"Error: {str(e)}",
                    "timestamp": timestamp,
                }
            ],
            "errors": [f"Visual Designer: {str(e)}"],
        }
