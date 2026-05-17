"""
TakhleeqX Supervisor Agent — Agent 6 in the pipeline.

Reviews the entire pipeline output, evaluates each agent's work quality,
assigns a campaign quality score (0-100), and provides actionable notes.

Demo Talking Point: The Supervisor Agent demonstrates AGENT OVERSIGHT — 
an autonomous quality-assurance layer that evaluates the output of all 
other agents. This is a key concept in multi-agent systems: having a 
"manager" agent that reviews subordinate agents' work.
"""

import json
import logging
from datetime import datetime, timezone
from openai import OpenAI
from backend.config import get_settings
from backend.agents.state import PipelineState
from backend.database import SessionLocal
from backend.models import Campaign, AgentExecutionLog, TrendCache

settings = get_settings()
logger = logging.getLogger("takhleeqx.agents.supervisor")

SUPERVISOR_PROMPT = """You are the Supervisor Agent for TakhleeqX, an AI marketing platform.

Your job is to review the COMPLETE output of a 5-agent marketing pipeline and provide a quality assessment.

## Restaurant Profile
- Name: {restaurant_name}
- Cuisine: {cuisine_type}
- City: {target_city}
- Tone: {brand_tone}

## Pipeline Outputs to Review

### Trend Scout Output
Local trends found: {local_trend_count}
Global trends found: {global_trend_count}
Synthesis: {trend_synthesis_preview}

### Strategy Planner Output
Campaign Name: {campaign_name}
Target Audience: {target_audience}
Content Pillars: {content_pillars}

### Content Writer Output
Posts Generated: {post_count}
Sample Caption: {sample_caption}

### Visual Designer Output
Images Generated: {visual_count}

### Campaign Publisher Output
Posts Published: {published_count}

## Your Task
Evaluate the entire pipeline and respond with ONLY this JSON:
{{
    "quality_score": <0-100 integer>,
    "overall_assessment": "<2-3 sentence summary of campaign quality>",
    "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
    "improvements": ["<suggestion 1>", "<suggestion 2>"],
    "agent_evaluations": {{
        "trend_scout": {{"score": <0-100>, "note": "<one line>"}},
        "strategy_planner": {{"score": <0-100>, "note": "<one line>"}},
        "content_writer": {{"score": <0-100>, "note": "<one line>"}},
        "visual_designer": {{"score": <0-100>, "note": "<one line>"}},
        "campaign_publisher": {{"score": <0-100>, "note": "<one line>"}}
    }},
    "brand_alignment_score": <0-100>,
    "trend_relevance_score": <0-100>,
    "content_creativity_score": <0-100>
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
        return {"quality_score": 75, "overall_assessment": cleaned[:500]}


def supervisor_node(state: PipelineState) -> dict:
    """
    LangGraph node for the Supervisor agent.
    
    Reviews all agent outputs, writes agent logs to DB, 
    caches trends to TrendCache, and evaluates quality.
    """
    logger.info("🧑‍💼 Supervisor agent starting...")
    timestamp = datetime.now(timezone.utc).isoformat()

    db = SessionLocal()
    try:
        # ─── Persist trends to TrendCache ──────────────────────
        local_trends = state.get("local_trends", [])
        global_trends = state.get("global_trends", [])
        synthesis = state.get("trend_synthesis", {})

        if local_trends:
            db.add(TrendCache(
                restaurant_id=state["restaurant_id"],
                query_type="local",
                data=local_trends,
            ))
        if global_trends:
            db.add(TrendCache(
                restaurant_id=state["restaurant_id"],
                query_type="global",
                data=global_trends,
            ))
        if synthesis:
            db.add(TrendCache(
                restaurant_id=state["restaurant_id"],
                query_type="synthesis",
                data=synthesis,
            ))

        # ─── Persist agent logs to AgentExecutionLog ───────────
        campaign_id = state.get("campaign_id")
        for log_entry in state.get("agent_logs", []):
            db.add(AgentExecutionLog(
                campaign_id=campaign_id,
                agent_name=log_entry.get("agent_name", "Unknown"),
                status=log_entry.get("status", "unknown"),
                message=log_entry.get("message", ""),
            ))

        db.commit()
        logger.info("✅ Trends cached and agent logs persisted to DB")

        # ─── LLM-based quality evaluation ──────────────────────
        strategy = state.get("strategy", {})
        posts = state.get("posts", [])
        visuals = state.get("visuals", [])
        published = state.get("published_posts", [])

        sample_caption = posts[0].get("caption", "N/A")[:200] if posts else "N/A"

        prompt = SUPERVISOR_PROMPT.format(
            restaurant_name=state["restaurant_name"],
            cuisine_type=state["cuisine_type"],
            target_city=state["target_city"],
            brand_tone=state["brand_tone"],
            local_trend_count=len(local_trends),
            global_trend_count=len(global_trends),
            trend_synthesis_preview=json.dumps(synthesis)[:300] if synthesis else "N/A",
            campaign_name=strategy.get("campaign_name", "N/A"),
            target_audience=strategy.get("target_audience", "N/A"),
            content_pillars=json.dumps(strategy.get("content_pillars", []))[:300],
            post_count=len(posts),
            sample_caption=sample_caption,
            visual_count=len(visuals),
            published_count=len(published),
        )

        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        evaluation = _parse_json_safe(response.choices[0].message.content)

        quality_score = evaluation.get("quality_score", 75)
        supervisor_notes = evaluation.get("overall_assessment", "Campaign reviewed.")

        # ─── Update campaign in DB with quality score ──────────
        if campaign_id:
            campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
            if campaign:
                campaign.quality_score = quality_score
                campaign.supervisor_notes = supervisor_notes
                db.commit()

        logger.info(f"✅ Supervisor completed — Quality Score: {quality_score}/100")

        return {
            "quality_score": quality_score,
            "supervisor_notes": supervisor_notes,
            "agent_evaluations": evaluation,
            "current_agent": "performance_predictor",
            "agent_logs": [
                {
                    "agent_name": "Supervisor",
                    "status": "done",
                    "message": f"Campaign quality score: {quality_score}/100. {supervisor_notes}",
                    "timestamp": timestamp,
                }
            ],
        }

    except Exception as e:
        logger.error(f"❌ Supervisor failed: {str(e)}")
        return {
            "quality_score": None,
            "supervisor_notes": f"Evaluation failed: {str(e)}",
            "agent_evaluations": {},
            "current_agent": "performance_predictor",
            "agent_logs": [
                {
                    "agent_name": "Supervisor",
                    "status": "error",
                    "message": f"Error: {str(e)}",
                    "timestamp": timestamp,
                }
            ],
            "errors": [f"Supervisor: {str(e)}"],
        }
    finally:
        db.close()
