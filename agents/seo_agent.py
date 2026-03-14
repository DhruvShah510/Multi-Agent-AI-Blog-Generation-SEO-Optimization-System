"""
agents/seo_agent.py — SEO Optimizer Agent (Node 4 of 4)

WHAT THIS AGENT DOES:
---------------------
This is the FINAL agent in the pipeline. It reads the polished blog post
from the Editor Agent and generates two key SEO elements:
  1. SEO Title       — a compelling title (max 60 characters)
  2. Meta Description — a summary for search engines (max 150 characters)

REAL-LIFE ANALOGY:
------------------
Like an SEO specialist at a digital marketing agency who takes a finished
article and writes the Google search snippet — the title and description
that appear in search results. These are critical for click-through rates.

HOW IT FITS IN LANGGRAPH:
--------------------------
  State coming IN  → { ..., edited_blog: "polished blog..." }
  State going OUT  → { ..., seo_title: "...", meta_description: "..." }

This is the LAST node before END. After this, the workflow is complete.
"""

from langchain_core.messages import HumanMessage
from graph.state import BlogState
from utils.llm_provider import get_llm
from utils.logger import log_agent_start, log_agent_done


def seo_agent(state: BlogState) -> dict:
    """
    LangGraph node function for the SEO Optimizer Agent.

    This node runs AFTER the Editor Agent. The state now contains all
    previous outputs: topic, outline, draft_blog, and edited_blog.

    Args:
        state: The current BlogState (all fields except seo_title and meta_description)

    Returns:
        dict with keys `seo_title` and `meta_description`
    """

    log_agent_start("SEO Agent", "Generating SEO title and meta description...")

    # We only need the final polished blog to generate SEO metadata
    edited_blog = state["edited_blog"]
    topic = state["topic"]

    llm = get_llm()

    # SHORT PROMPT — very specific format request so we can parse the output reliably
    # We use "SEO Title:" and "Meta Description:" as markers for easy parsing
    prompt = f"""Generate SEO metadata for this blog post about "{topic}".

Blog post:
{edited_blog[:500]}

Return EXACTLY in this format (no extra text):
SEO Title: [title here, max 60 characters]
Meta Description: [description here, max 150 characters]"""

    response = llm.invoke([HumanMessage(content=prompt)])
    output = response.content.strip()

    # Parse the LLM output to extract title and description
    # We look for the specific label markers we requested
    seo_title = ""
    meta_description = ""

    for line in output.split("\n"):
        line = line.strip()
        if line.lower().startswith("seo title:"):
            # Extract everything after "SEO Title: "
            seo_title = line.split(":", 1)[-1].strip()
        elif line.lower().startswith("meta description:"):
            # Extract everything after "Meta Description: "
            meta_description = line.split(":", 1)[-1].strip()

    # Fallback: if parsing fails, use the raw output as the title
    if not seo_title:
        seo_title = output.split("\n")[0][:60]
    if not meta_description:
        meta_description = output[:150]

    log_agent_done("SEO Agent")

    # Return the two SEO fields — these are the last pieces to complete the state
    return {
        "seo_title": seo_title,
        "meta_description": meta_description,
    }
