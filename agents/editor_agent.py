"""
agents/editor_agent.py — Editor Agent (Node 3 of 4)

WHAT THIS AGENT DOES:
---------------------
This is the THIRD agent. It takes the raw draft blog post from the Writer Agent
and improves it — fixing grammar, improving clarity, and making the flow smoother.

REAL-LIFE ANALOGY:
------------------
Like a senior editor at a magazine who reviews a journalist's draft,
corrects awkward phrasing, removes redundant sentences, and improves readability
— without completely rewriting the article.

HOW IT FITS IN LANGGRAPH:
--------------------------
  State coming IN  → { ..., draft_blog: "raw draft here..." }
  State going OUT  → { ..., edited_blog: "polished version here..." }

The agent reads `draft_blog` and writes `edited_blog`.
It does NOT re-read the topic or outline — it only works with what was written.
"""

from langchain_core.messages import HumanMessage
from graph.state import BlogState
from utils.llm_provider import get_llm
from utils.logger import log_agent_start, log_agent_done


def editor_agent(state: BlogState) -> dict:
    """
    LangGraph node function for the Editor Agent.

    This node runs AFTER the Writer Agent. The state now contains:
    topic, outline, and draft_blog.

    Args:
        state: The current BlogState (contains topic + outline + draft_blog)

    Returns:
        dict with key `edited_blog` → the edited, polished blog post
    """

    log_agent_start("Editor Agent", "Editing and polishing the blog...")

    # The editor only needs the raw draft to do its job
    draft_blog = state["draft_blog"]

    llm = get_llm()

    # SHORT PROMPT — ask to improve but NOT expand the text
    # "Do not add new sections" prevents the LLM from inflating the response
    prompt = f"""Edit the following blog post for grammar, clarity, and flow.

Rules:
- Fix grammar and spelling errors
- Improve sentence clarity where needed
- Do NOT add new sections or expand the content significantly
- Do NOT add a title
- Keep the same number of paragraphs
- Return only the edited blog text

Blog post to edit:
{draft_blog}"""

    response = llm.invoke([HumanMessage(content=prompt)])
    edited_blog = response.content.strip()

    log_agent_done("Editor Agent")

    # Return the edited version as the new `edited_blog` field in state
    return {"edited_blog": edited_blog}
