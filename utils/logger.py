"""
utils/logger.py — Terminal Logging Utility

PURPOSE:
--------
Provides simple, colorful terminal output so users can visually track
which agent is currently running in the LangGraph pipeline.

REAL-LIFE ANALOGY:
------------------
Like a factory assembly line status board:
  [Station 1] Cutting in progress...
  [Station 2] Welding in progress...
  [Station 3] Painting in progress...

This gives users confidence that the system is working, not frozen.
"""


def log_agent_start(agent_name: str, action: str):
    """
    Prints a formatted start message when an agent begins its work.

    Args:
        agent_name: The display name of the agent (e.g., "Planner Agent")
        action: What the agent is doing (e.g., "Generating outline...")

    Example output:
        ──────────────────────────────────────
        [Planner Agent] Generating outline...
        ──────────────────────────────────────
    """
    separator = "─" * 50
    print(f"\n{separator}")
    print(f"[{agent_name}] {action}")
    print(separator)


def log_agent_done(agent_name: str):
    """
    Prints a confirmation message when an agent finishes its task.

    Args:
        agent_name: The display name of the agent

    Example output:
        ✅ [Planner Agent] Done.
    """
    print(f"[DONE] [{agent_name}]")


def log_workflow_start():
    """Prints a banner at the start of the entire LangGraph workflow."""
    print("\n" + "═" * 50)
    print("  >> Starting LangGraph Workflow...")
    print("═" * 50)


def log_workflow_complete():
    """Prints a success banner when the entire workflow finishes."""
    print("\n" + "═" * 50)
    print("  ** Workflow Complete! **")
    print("═" * 50 + "\n")


def log_section(title: str, content: str):
    """
    Prints a labeled section in the terminal for easy reading.

    Args:
        title: Section label (e.g., "OUTLINE")
        content: The text content to display

    Example output:
        ┌─── OUTLINE ───────────────────────────────────┐
        1. Introduction
        2. What is AI?
        ...
    """
    print(f"\n┌─── {title.upper()} {'─' * (44 - len(title))}┐")
    print(content)
    print("└" + "─" * 49 + "┘")
