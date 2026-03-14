"""
agents/writer_agent.py — Writer Agent (Node 2 of 4)

WHAT THIS AGENT DOES:
---------------------
This is the SECOND agent. It receives both the topic and the outline
(created by the Planner Agent) and writes a short draft blog post.

REAL-LIFE ANALOGY:
------------------
Like a journalist who receives the article structure from the editor-in-chief
and then writes the actual paragraphs based on those section headings.

HOW IT FITS IN LANGGRAPH:
--------------------------
  State coming IN  → { topic: "...", outline: "1. Intro\n2. ..." }
  State going OUT  → { ..., draft_blog: "Here is the draft blog..." }

The agent reads `topic` and `outline` from state, then writes `draft_blog`.
"""

from langchain_core.messages import HumanMessage
from graph.state import BlogState
from utils.llm_provider import get_llm
from utils.logger import log_agent_start, log_agent_done


def writer_agent(state: BlogState) -> dict:
    """
    LangGraph node function for the Writer Agent.

    This node runs AFTER the Planner Agent. By the time this node runs,
    the state already contains both `topic` and `outline`.

    Args:
        state: The current BlogState (contains topic + outline)

    Returns:
        dict with key `draft_blog` → the raw first-draft blog post
    """

    log_agent_start("Writer Agent", "Writing draft blog post...")

    # Read the inputs we need from the shared state
    topic = state["topic"]
    outline = state["outline"]

    llm = get_llm()

    # SHORT PROMPT — we explicitly ask for 3-5 short paragraphs
    # to avoid generating a long article (which wastes tokens on free tier)
    prompt = f"""Write a short blog post about "{topic}" using this outline:

{outline}

Rules:
- Write exactly 3 to 5 short paragraphs
- Each paragraph should be 2–3 sentences max
- Keep the total word count under 250 words
- Write in a friendly, informative tone
- Do not add a title

Start writing directly."""

    response = llm.invoke([HumanMessage(content=prompt)])
    draft_blog = response.content.strip()

    log_agent_done("Writer Agent")

    # Return only the new field this agent produced.
    # The existing state fields (topic, outline) are preserved automatically by LangGraph.
    return {"draft_blog": draft_blog}
