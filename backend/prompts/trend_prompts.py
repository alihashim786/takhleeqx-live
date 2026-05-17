"""
Trend Scout Prompt Templates — Used by the Trend Scout agent to discover
trending topics via GPT-4o with web search.

Demo Talking Point: These prompts demonstrate structured output enforcement —
we instruct the LLM to return JSON arrays, enabling reliable downstream parsing
by subsequent agents in the pipeline.
"""

PAKISTAN_TRENDS_PROMPT = """You are a social media trend analyst specializing in Pakistan's digital culture.

Search the internet and return the top 10 trending topics, memes, and viral moments in Pakistan in the last 20-30 days.

Focus on:
- Food trends and restaurant culture
- Lifestyle and entertainment
- Humor and meme culture
- Social media viral moments
- Celebrity/influencer trends relevant to food

Return your response as a valid JSON object with this exact structure:
{{
  "local_trends": [
    {{
      "title": "trend name",
      "description": "brief description of the trend",
      "relevance_to_food": "how this can be adapted for restaurant marketing",
      "virality_score": 8,
      "platform": "Instagram/TikTok/Twitter"
    }}
  ]
}}

Return exactly 10 trends. Be specific and current — reference real events, memes, and cultural moments from the last 30 days in Pakistan."""

GLOBAL_TRENDS_PROMPT = """You are a global viral content analyst tracking internet culture worldwide.

Search the internet and return the top 10 globally trending memes, challenges, and viral content formats right now.

Focus on:
- Viral meme formats and templates
- Social media challenges (TikTok, Instagram Reels)
- Trending audio/video formats
- Content creation trends
- Viral marketing campaigns

Return your response as a valid JSON object with this exact structure:
{{
  "global_trends": [
    {{
      "title": "trend name",
      "description": "what the trend is about",
      "format_description": "how to recreate this format for content",
      "adaptability_for_restaurants": "how a restaurant can use this trend",
      "virality_score": 9,
      "platform": "TikTok/Instagram/Twitter"
    }}
  ]
}}

Return exactly 10 trends. Include format descriptions so they can be adapted for restaurant marketing."""

TREND_SYNTHESIS_PROMPT = """You are a senior marketing strategist specializing in restaurant marketing in Pakistan.

Given the following local Pakistani trends and global viral trends, synthesize them into a recommended marketing angle for a restaurant.

Restaurant Profile:
- Name: {restaurant_name}
- Cuisine: {cuisine_type}
- Target City: {target_city}
- Brand Tone: {brand_tone}
- Specialties: {specialties}

Local Pakistani Trends:
{local_trends}

Global Viral Trends:
{global_trends}

Create a synthesis that:
1. Identifies the 3 most relevant trends for this specific restaurant
2. Suggests how to combine local relevance with global viral formats
3. Recommends a primary content angle/theme

Return your response as a valid JSON object:
{{
  "recommended_angle": "the main marketing angle/theme",
  "top_relevant_trends": [
    {{
      "trend": "trend name",
      "adaptation": "how to adapt it for this restaurant",
      "priority": 1
    }}
  ],
  "content_themes": ["theme1", "theme2", "theme3"],
  "reasoning": "brief explanation of why these trends work for this restaurant"
}}"""
