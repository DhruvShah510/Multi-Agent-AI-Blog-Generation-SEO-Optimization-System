"""
graph/state.py — Shared State Definition for the LangGraph Blog Generator

WHAT IS LANGGRAPH STATE?
------------------------
In LangGraph, "state" is like a shared notebook that every agent (node) can read and write.

Think of it like a relay race baton:
  - Runner 1 (Planner) receives the baton (state), writes an outline, passes it on.
  - Runner 2 (Writer) receives the same baton, reads the outline, writes a draft, passes it on.
  - ... and so on until the final agent finishes.

The state is a Python TypedDict (or Pydantic model). Each key represents one piece
of information that flows through the pipeline.

HOW STATE FLOWS BETWEEN AGENTS:
--------------------------------
  START
    └─► planner_agent  reads: topic        writes: outline
          └─► writer_agent   reads: outline      writes: draft_blog
                └─► editor_agent   reads: draft_blog   writes: edited_blog
                      └─► seo_agent      reads: edited_blog  writes: seo_title, meta_description
                            └─► END
"""

from typing import TypedDict


# BlogState is the single shared state object that all agents use.
# Think of it as a "form" being filled out step by step by different team members.
class BlogState(TypedDict):
    """
    Shared state that flows through every node (agent) in the LangGraph workflow.

    Each field is filled in by a specific agent:
      - topic           → provided by the user (input)
      - outline         → filled by Planner Agent
      - draft_blog      → filled by Writer Agent
      - edited_blog     → filled by Editor Agent
      - seo_title       → filled by SEO Agent
      - meta_description → filled by SEO Agent
    """

    # The blog topic the user wants to write about
    # Example: "Machine Learning in Healthcare"
    topic: str

    # A structured outline with 3–5 sections
    # Example: "1. Introduction\n2. What is ML?\n3. Benefits\n4. Examples\n5. Conclusion"
    outline: str

    # The raw draft blog post written by the Writer Agent
    draft_blog: str

    # The polished version of the blog after editing
    edited_blog: str

    # SEO-optimized blog title (max 60 characters)
    # Example: "How Machine Learning is Transforming Healthcare"
    seo_title: str

    # Short meta description for search engines (max 150 characters)
    # Example: "Discover how ML is revolutionizing diagnostics and patient care in modern healthcare systems."
    meta_description: str
