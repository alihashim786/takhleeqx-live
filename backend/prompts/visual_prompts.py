"""
Visual Designer Prompt Templates — Used by the Visual Designer agent
to generate DALL-E 3 image prompts from post content.

Demo Talking Point: This prompt transforms text content into visual specifications,
demonstrating how tool-using agents (DALL-E 3) require specialized prompt engineering
distinct from text LLM prompts.
"""

IMAGE_PROMPT_TEMPLATE = """Create a stunning, professional social media post image for a restaurant.

Restaurant: {restaurant_name}
Cuisine: {cuisine_type}
Brand Tone: {brand_tone}
Visual Style: {visual_style}

Post Context: {caption_summary}
Image Suggestion: {image_suggestion}

Requirements:
- Professional food photography or lifestyle aesthetic with a highly NATURAL element
- Make the image look completely naturally made, realistic, and unpolished in a good way
- Add some subtle noise and film grain to make it look more appealing and authentic
- Vibrant, appetizing colors but grounded in reality
- Modern, Instagram-worthy composition
- No text overlays (the caption will be added separately)
- Warm, inviting atmosphere
- {brand_tone} mood and feel

Style: Professional food photography, subtle film grain, natural lighting, realistic textures, cinematic lighting, shallow depth of field, social media optimized."""

MEME_PROMPT_TEMPLATE = """Create a hilarious, viral-style meme image for a restaurant social media post.

Restaurant: {restaurant_name}
Cuisine: {cuisine_type}
Brand Tone: {brand_tone}
Visual Style: {visual_style}

Post Context: {caption_summary}
Image Suggestion: {image_suggestion}

Requirements:
- The image MUST be a relatable meme format tailored to the product being marketed or a current trend.
- Include bold, impactful text directly on the image acting as the meme caption (e.g. Impact font or modern TikTok style text).
- Make it look highly authentic, slightly grainy (add noise), and naturally made like a real user posted it.
- Keep the humor relevant to food, dining out, or Pakistani culture.
- {brand_tone} mood and feel.

Style: Viral meme format, internet culture, relatable humor, natural photo base with bold text overlay, slightly noisy aesthetic."""
