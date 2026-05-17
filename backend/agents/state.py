"""
TakhleeqX Agent State Schema — The shared TypedDict that flows through
the entire LangGraph StateGraph pipeline.

Demo Talking Point: This state object is the backbone of the agentic system —
it demonstrates STATE MANAGEMENT, the key differentiator between simple API
chains and true agent orchestration. Each agent reads from and writes to this
shared state, enabling context preservation across the entire pipeline.
"""

from typing import TypedDict, Optional, Annotated
from operator import add


class AgentLog(TypedDict):
    """A single log entry from an agent's execution."""
    agent_name: str
    status: str  # idle, running, done, error
    message: str
    timestamp: str


class PipelineState(TypedDict):
    """
    Shared state that flows through all agents in the LangGraph pipeline.
    Each agent reads what it needs and writes its output here.
    """

    # ─── Input: Restaurant Profile ─────────────────────────────
    restaurant_id: int
    restaurant_name: str
    cuisine_type: str
    target_city: str
    brand_tone: str
    posting_frequency: str
    description: str
    specialties: str

    # ─── User Context ──────────────────────────────────────────
    user_id: int
    campaign_id: Optional[int]

    # ─── Agent 1 Output: Trend Scout ──────────────────────────
    local_trends: Optional[list]
    global_trends: Optional[list]
    trend_synthesis: Optional[dict]

    # ─── Agent 2 Output: Strategy Planner ─────────────────────
    strategy: Optional[dict]

    # ─── Agent 3 Output: Content Writer ───────────────────────
    posts: Optional[list]

    # ─── Agent 4 Output: Visual Designer ──────────────────────
    visuals: Optional[list]

    # ─── Agent 5 Output: Reel Producer ────────────────────────
    reels: Optional[list]

    # ─── Agent 6 Output: Campaign Publisher ───────────────────
    published_posts: Optional[list]

    # ─── Agent 6 Output: Supervisor ───────────────────────────
    quality_score: Optional[int]         # 0-100 quality score
    supervisor_notes: Optional[str]      # Overall assessment text
    agent_evaluations: Optional[dict]    # Per-agent quality assessment

    # ─── Agent 7 Output: Performance Predictor ────────────────
    predicted_analytics: Optional[dict]  # Predicted reach, engagement, etc.

    # ─── Pipeline Metadata ────────────────────────────────────
    current_agent: str
    agent_logs: Annotated[list, add]  # Append-only log of all agent activities
    errors: Annotated[list, add]  # Append-only error list
    pipeline_status: str  # pending, running, completed, failed
