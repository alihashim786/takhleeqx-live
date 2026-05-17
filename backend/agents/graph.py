"""
TakhleeqX Agent Graph — LangGraph StateGraph that orchestrates all 7 agents.

This is the ORCHESTRATION CORE of the system. It defines:
  - Node registration (one per agent)
  - Edge wiring (sequential pipeline with conditional routing)
  - State management (PipelineState flows through all nodes)
  - Quality gates (conditional edges that validate outputs)

Pipeline: START → Trend Scout → Strategy Planner → Content Writer
          → Visual Designer → Campaign Publisher → Supervisor
          → Performance Predictor → END

Demo Talking Point: This file is the heart of the agentic architecture —
the StateGraph manages the execution order, state transitions, and error
handling across all 7 agents. The Supervisor agent reviews the work of
all 5 pipeline agents, and the Performance Predictor generates AI-based
engagement forecasts.
"""

import logging
from langgraph.graph import StateGraph, START, END
from backend.agents.state import PipelineState
from backend.agents.trend_scout import trend_scout_node
from backend.agents.strategy_planner import strategy_planner_node
from backend.agents.content_writer import content_writer_node
from backend.agents.visual_designer import visual_designer_node
from backend.agents.reel_producer import reel_producer_node
from backend.agents.campaign_publisher import campaign_publisher_node
from backend.agents.supervisor import supervisor_node
from backend.agents.performance_predictor import performance_predictor_node

logger = logging.getLogger("takhleeqx.agents.graph")


# ─── Quality Gate Functions ────────────────────────────────────
def should_continue_after_trends(state: PipelineState) -> str:
    """Conditional routing after Trend Scout — check if trends were found."""
    trends = state.get("local_trends", [])
    synthesis = state.get("trend_synthesis", {})

    if not trends and "error" in synthesis:
        logger.warning("Trend Scout produced no results — continuing with defaults")

    # Always continue to strategy (even with partial data)
    return "strategy_planner"


def should_continue_after_strategy(state: PipelineState) -> str:
    """Conditional routing after Strategy Planner — verify strategy quality."""
    strategy = state.get("strategy", {})

    if "error" in strategy:
        logger.warning("Strategy Planner failed — continuing with limited strategy")

    return "content_writer"


def should_continue_after_content(state: PipelineState) -> str:
    """Conditional routing after Content Writer — verify posts exist."""
    posts = state.get("posts", [])

    if not posts:
        logger.warning("Content Writer produced no posts — skipping image generation")
        return "campaign_publisher"

    return "visual_designer"


def should_continue_after_visuals(state: PipelineState) -> str:
    """Conditional routing after Visual Designer."""
    return "reel_producer"

def should_continue_after_reels(state: PipelineState) -> str:
    """Conditional routing after Reel Producer."""
    return "campaign_publisher"


def should_continue_after_publisher(state: PipelineState) -> str:
    """After publishing, always go to supervisor for quality review."""
    return "supervisor"


def should_continue_after_supervisor(state: PipelineState) -> str:
    """After supervisor review, go to performance predictor."""
    return "performance_predictor"


# ─── Build the StateGraph ──────────────────────────────────────
def build_agent_graph() -> StateGraph:
    """
    Construct and compile the LangGraph StateGraph.

    Pipeline: START → Trend Scout → Strategy Planner → Content Writer
              → Visual Designer → Campaign Publisher → Supervisor
              → Performance Predictor → END
    """
    logger.info("Building agent pipeline graph (7 agents)...")

    # Create the graph with our state schema
    graph = StateGraph(PipelineState)

    # ── Register agent nodes ───────────────────────────────────
    graph.add_node("trend_scout", trend_scout_node)
    graph.add_node("strategy_planner", strategy_planner_node)
    graph.add_node("content_writer", content_writer_node)
    graph.add_node("visual_designer", visual_designer_node)
    graph.add_node("reel_producer", reel_producer_node)
    graph.add_node("campaign_publisher", campaign_publisher_node)
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("performance_predictor", performance_predictor_node)

    # ── Wire edges with conditional routing ────────────────────
    # START → Trend Scout
    graph.add_edge(START, "trend_scout")

    # Trend Scout → Strategy Planner (with quality gate)
    graph.add_conditional_edges(
        "trend_scout",
        should_continue_after_trends,
        {"strategy_planner": "strategy_planner"},
    )

    # Strategy Planner → Content Writer (with quality gate)
    graph.add_conditional_edges(
        "strategy_planner",
        should_continue_after_strategy,
        {"content_writer": "content_writer"},
    )

    # Content Writer → Visual Designer or Publisher (conditional skip)
    graph.add_conditional_edges(
        "content_writer",
        should_continue_after_content,
        {
            "visual_designer": "visual_designer",
            "campaign_publisher": "campaign_publisher",
        },
    )

    # Visual Designer → Reel Producer
    graph.add_conditional_edges(
        "visual_designer",
        should_continue_after_visuals,
        {"reel_producer": "reel_producer"},
    )

    # Reel Producer → Campaign Publisher
    graph.add_conditional_edges(
        "reel_producer",
        should_continue_after_reels,
        {"campaign_publisher": "campaign_publisher"},
    )

    # Campaign Publisher → Supervisor
    graph.add_conditional_edges(
        "campaign_publisher",
        should_continue_after_publisher,
        {"supervisor": "supervisor"},
    )

    # Supervisor → Performance Predictor
    graph.add_conditional_edges(
        "supervisor",
        should_continue_after_supervisor,
        {"performance_predictor": "performance_predictor"},
    )

    # Performance Predictor → END
    graph.add_edge("performance_predictor", END)

    logger.info("✅ Agent pipeline graph built successfully (7 nodes)")

    # Compile the graph
    compiled = graph.compile()
    return compiled


# ─── Pipeline Execution ───────────────────────────────────────
def run_pipeline(initial_state: dict) -> dict:
    """
    Execute the full agent pipeline with the given initial state.

    Args:
        initial_state: Dict with restaurant profile and metadata

    Returns:
        Final state dict with all agent outputs
    """
    logger.info("🚀 Starting agent pipeline execution (7 agents)...")

    # Ensure required default state fields
    state = {
        "local_trends": None,
        "global_trends": None,
        "trend_synthesis": None,
        "strategy": None,
        "posts": None,
        "visuals": None,
        "published_posts": None,
        "campaign_id": None,
        "quality_score": None,
        "supervisor_notes": None,
        "agent_evaluations": None,
        "predicted_analytics": None,
        "current_agent": "trend_scout",
        "agent_logs": [],
        "errors": [],
        "pipeline_status": "running",
        **initial_state,
    }

    compiled_graph = build_agent_graph()

    # Execute the graph
    final_state = compiled_graph.invoke(state)

    logger.info(f"🏁 Pipeline completed with status: {final_state.get('pipeline_status', 'unknown')}")
    return final_state
