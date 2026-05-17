"""
Reel Producer Prompts — Used to generate scripts and scenes for
Pakistani-style Reels/TikTok videos using Urdu dialogues.
"""

REEL_SCRIPT_PROMPT = """You are an expert Pakistani social media marketer and Gen-Z meme creator.

We need to generate a script for a funny viral Reel/TikTok using a "Chat Interaction" video template.
Restaurant: {restaurant_name}
Cuisine: {cuisine_type}
City: {target_city}
Brand Tone: {brand_tone}
Post Context: {caption_summary}

Requirements:
1. The video simulates a funny chat conversation between two people. Person 1 is "Shahbaz" and Person 2 is "Trump".
2. The dialogue MUST be highly relevant to Pakistani food culture (desi humor, foodie struggles, etc.) and fit the product.
3. The conversation MUST be in casual Roman Urdu / Minglish. 
   Example:
   Shahbaz: "trump jani biryani ka mood ho raha hai?"
   Trump: "han jani lekin paise nae hai"
   Shahbaz: "phir jab paise ho to btayi :)"
4. Keep the messages very short, punchy, and funny.
5. Provide the brand name and a catchy Urdu/Minglish tagline to be shown at the very end of the video.

Output ONLY valid JSON in this format (no markdown, no quotes outside JSON):
{{
    "shahbaz_msg_1": "<Shahbaz's first funny message>",
    "trump_msg_1": "<Trump's reply>",
    "shahbaz_msg_2": "<Shahbaz's final savage or funny reply>",
    "brand_name": "<The brand name, e.g. {restaurant_name}>",
    "tagline": "<A short catchy tagline, e.g. 'kuch to khas hai isme'>"
}}
"""
