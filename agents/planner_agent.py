"""
agents/planner_agent.py — Content Planner Agent (Node 1 of 4)

WHAT THIS AGENT DOES:
---------------------
This is the FIRST agent in the pipeline. It receives just the blog topic
from the user and produces a structured outline with 3–5 sections.

REAL-LIFE ANALOGY:
------------------
Think of this like a senior journalist at a newspaper who first sketches out
the article structure before handing it to a writer. They say:
  "Here's what sections we need: intro, background, main points, examples, conclusion."

HOW IT FITS IN LANGGRAPH:
--------------------------
  State coming IN  → { topic: "AI in Healthcare" }
  State going OUT  → { topic: "AI in Healthcare", outline: "1. Intro\n2. ..." }

The agent only ADDS the `outline` field. All existing fields remain untouched.
This is the key LangGraph pattern — each node returns only what it changed.
"""

from langchain_core.messages import HumanMessage
from graph.state import BlogState
from utils.llm_provider import get_llm
from utils.logger import log_agent_start, log_agent_done


def planner_agent(state: BlogState) -> dict:
    """
    LangGraph node function for the Content Planner Agent.

    In LangGraph, every node function:
      1. Receives the full current state as input
      2. Does its work (calls LLM, runs logic, etc.)
      3. Returns a dict with ONLY the fields it wants to update

    LangGraph automatically merges the returned dict back into the shared state.

    Args:
        state: The current BlogState (at this point, only `topic` is set)

    Returns:
        dict with key `outline` → the generated blog outline
    """

    log_agent_start("Planner Agent", "Generating outline...")

    # Get the topic from the shared state
    # At this point, only `topic` has been set (by the user)
    topic = state["topic"]

    # Initialize the LLM (OpenAI gpt-4o-mini or Anthropic claude-3-haiku)
    llm = get_llm()

    # SHORT PROMPT — kept minimal to save API tokens (important for free-tier users)
    # The prompt is specific and structured so the LLM returns a clean outline
    prompt = f"""Create a short blog outline for the topic: "{topic}"

Format:
1. Introduction
2. What is {topic}
3. Key Benefits or Features
4. Real-world Example
5. Conclusion

Keep each section title short (5-7 words max). Return only the numbered list."""

    # Call the LLM with our prompt
    # HumanMessage wraps the prompt as a user message in the chat format
    response = llm.invoke([HumanMessage(content=prompt)])

    # Extract the text content from the LLM response
    outline = response.content.strip()

    log_agent_done("Planner Agent")

    # Return only the field this agent is responsible for.
    # LangGraph merges this into the full state automatically.
    # Think of it like: state["outline"] = outline
    return {"outline": outline}
