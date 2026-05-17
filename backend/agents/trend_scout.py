"""
TakhleeqX Trend Scout Agent — Agent 1 in the pipeline.

Uses GPT-4o with web search to discover:
  - Top 10 Pakistani food/lifestyle trends (last 30 days)
  - Top 10 globally viral memes/content formats
  - Synthesized recommendation tailored to the restaurant

Demo Talking Point: The Trend Scout demonstrates TOOL USE — it calls GPT-4o
with the web_search tool enabled, making it an agent that can access real-time
internet data rather than relying on training data cutoffs.
"""

import os
import json
import logging
from datetime import datetime, timezone
from openai import OpenAI
from backend.config import get_settings
from backend.agents.state import PipelineState
from backend.prompts.trend_prompts import (
    PAKISTAN_TRENDS_PROMPT,
    GLOBAL_TRENDS_PROMPT,
    TREND_SYNTHESIS_PROMPT,
)

settings = get_settings()
logger = logging.getLogger("takhleeqx.agents.trend_scout")


def _call_openai_with_search(prompt: str) -> str:
    """Call GPT-4o with web search enabled for real-time trend data."""
    api_key = os.environ.get("OPENAI_API_KEY", settings.OPENAI_API_KEY)
    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-4o",
        tools=[{"type": "web_search_preview"}],
        input=prompt,
    )

    return response.output_text


def _parse_json_response(text: str) -> dict:
    """Extract JSON from LLM response, handling markdown code blocks."""
    # Strip markdown code fences if present
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        # Remove first line (```json or ```) and last line (```)
        lines = [l for l in lines[1:] if not l.strip() == "```"]
        cleaned = "\n".join(lines)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to find JSON within the text
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        if start != -1 and end > start:
            try:
                return json.loads(cleaned[start:end])
            except json.JSONDecodeError:
                pass
        logger.warning("Failed to parse JSON from response, returning raw text")
        return {"raw_response": cleaned}


def trend_scout_node(state: PipelineState) -> dict:
    """
    LangGraph node function for the Trend Scout agent.

    Executes two parallel web searches (Pakistan local + global trends),
    then synthesizes them into a recommended angle for the restaurant.
    """
    logger.info("🔍 Trend Scout agent starting...")
    timestamp = datetime.now(timezone.utc).isoformat()

    try:
        # ── Sub-prompt A: Pakistan Local Trends ─────────────────
        logger.info("Searching Pakistan local trends...")
        local_response = _call_openai_with_search(PAKISTAN_TRENDS_PROMPT)
        local_data = _parse_json_response(local_response)
        local_trends = local_data.get("local_trends", [])

        # ── Sub-prompt B: Global Viral Trends ───────────────────
        logger.info("Searching global viral trends...")
        global_response = _call_openai_with_search(GLOBAL_TRENDS_PROMPT)
        global_data = _parse_json_response(global_response)
        global_trends = global_data.get("global_trends", [])

        # ── Synthesis Prompt: Fuse trends for restaurant ────────
        logger.info("Synthesizing trends for restaurant profile...")
        synthesis_prompt = TREND_SYNTHESIS_PROMPT.format(
            restaurant_name=state["restaurant_name"],
            cuisine_type=state["cuisine_type"],
            target_city=state["target_city"],
            brand_tone=state["brand_tone"],
            specialties=state.get("specialties", "various dishes"),
            local_trends=json.dumps(local_trends, indent=2),
            global_trends=json.dumps(global_trends, indent=2),
        )

        api_key = os.environ.get("OPENAI_API_KEY", settings.OPENAI_API_KEY)
        client = OpenAI(api_key=api_key)
        synthesis_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": synthesis_prompt}],
            temperature=0.7,
        )
        synthesis_text = synthesis_response.choices[0].message.content
        trend_synthesis = _parse_json_response(synthesis_text)

        # Save to local file
        os.makedirs("trends_data", exist_ok=True)
        filename = f"trends_data/trends_{state.get('restaurant_name', 'unknown').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({
                "local_trends": local_trends,
                "global_trends": global_trends,
                "synthesis": trend_synthesis
            }, f, indent=4, ensure_ascii=False)
        logger.info(f"💾 Saved trends locally to {filename}")

        logger.info("✅ Trend Scout completed successfully")

        return {
            "local_trends": local_trends,
            "global_trends": global_trends,
            "trend_synthesis": trend_synthesis,
            "current_agent": "strategy_planner",
            "agent_logs": [
                {
                    "agent_name": "Trend Scout",
                    "status": "done",
                    "message": f"Found {len(local_trends)} local and {len(global_trends)} global trends. Synthesized recommendation ready.",
                    "timestamp": timestamp,
                }
            ],
        }

    except Exception as e:
        logger.error(f"❌ Trend Scout failed: {str(e)}")
        return {
            "local_trends": [],
            "global_trends": [],
            "trend_synthesis": {"error": str(e)},
            "current_agent": "strategy_planner",
            "agent_logs": [
                {
                    "agent_name": "Trend Scout",
                    "status": "error",
                    "message": f"Error: {str(e)}",
                    "timestamp": timestamp,
                }
            ],
            "errors": [f"Trend Scout: {str(e)}"],
        }
