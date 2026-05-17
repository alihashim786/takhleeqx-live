"""
TakhleeqX Strategy Planner Agent — Agent 2 in the pipeline.

Receives restaurant profile + trend synthesis → produces a complete campaign
strategy with content pillars, schedule, and messaging.

Demo Talking Point: The Strategy Planner demonstrates AGENT CHAINING — it
consumes the structured output from Agent 1 (Trend Scout) and transforms it
into an actionable plan that Agent 3 (Content Writer) can execute, showing
how agents collaborate through shared state.
"""

import json
import logging
from datetime import datetime, timezone
from openai import OpenAI
from backend.config import get_settings
from backend.agents.state import PipelineState
from backend.prompts.strategy_prompts import STRATEGY_PROMPT

settings = get_settings()
logger = logging.getLogger("takhleeqx.agents.strategy_planner")


def strategy_planner_node(state: PipelineState) -> dict:
    """
    LangGraph node function for the Strategy Planner agent.

    Takes restaurant profile + trends → produces campaign strategy.
    """
    logger.info("📋 Strategy Planner agent starting...")
    timestamp = datetime.now(timezone.utc).isoformat()

    try:
        # Build the trend analysis summary for the prompt
        trend_analysis = json.dumps(
            {
                "synthesis": state.get("trend_synthesis", {}),
                "top_local_trends": state.get("local_trends", [])[:5],
                "top_global_trends": state.get("global_trends", [])[:5],
            },
            indent=2,
        )

        prompt = STRATEGY_PROMPT.format(
            restaurant_name=state["restaurant_name"],
            cuisine_type=state["cuisine_type"],
            target_city=state["target_city"],
            brand_tone=state["brand_tone"],
            posting_frequency=state.get("posting_frequency", "3x/week"),
            description=state.get("description", "A popular local restaurant"),
            specialties=state.get("specialties", "various dishes"),
            trend_analysis=trend_analysis,
        )

        api_key = os.environ.get("OPENAI_API_KEY", settings.OPENAI_API_KEY)
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        response_text = response.choices[0].message.content.strip()

        # Parse JSON from response
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            lines = [l for l in lines[1:] if l.strip() != "```"]
            response_text = "\n".join(lines)

        try:
            strategy = json.loads(response_text)
        except json.JSONDecodeError:
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            strategy = json.loads(response_text[start:end])

        logger.info(f"✅ Strategy Planner completed: {strategy.get('campaign_name', 'Unnamed')}")

        return {
            "strategy": strategy,
            "current_agent": "content_writer",
            "agent_logs": [
                {
                    "agent_name": "Strategy Planner",
                    "status": "done",
                    "message": f"Campaign '{strategy.get('campaign_name', 'Unnamed')}' created with {len(strategy.get('content_pillars', []))} content pillars.",
                    "timestamp": timestamp,
                }
            ],
        }

    except Exception as e:
        logger.error(f"❌ Strategy Planner failed: {str(e)}")
        return {
            "strategy": {"error": str(e)},
            "current_agent": "content_writer",
            "agent_logs": [
                {
                    "agent_name": "Strategy Planner",
                    "status": "error",
                    "message": f"Error: {str(e)}",
                    "timestamp": timestamp,
                }
            ],
            "errors": [f"Strategy Planner: {str(e)}"],
        }
