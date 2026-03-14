"""
run_demo.py — Terminal Runner for the LangGraph Blog Generator

HOW TO USE:
-----------
    python run_demo.py              # Interactive mode (asks for topic)
    python run_demo.py --diagram    # Generate + save the workflow diagram PNG

PURPOSE:
--------
This script lets you run the entire LangGraph pipeline from the terminal
without needing to open the Streamlit web app.

Useful for:
  - Quick testing of the workflow
  - Demonstrating to teammates in a terminal
  - Debugging individual agents

FLOW:
-----
  User enters topic
      │
      ▼
  run_workflow(topic) is called
      │
      ▼
  LangGraph runs all 4 agents in sequence
      │
      ▼
  Final state is printed to terminal
"""

import sys
import os

# Ensure the project root is on the Python path
# This allows imports like `from graph.workflow import run_workflow` to work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graph.workflow import run_workflow, save_workflow_diagram
from utils.logger import log_section


def main():
    """
    Main entry point for the terminal demo.

    Handles two modes:
    1. --diagram flag: generates and saves the workflow diagram PNG
    2. Normal mode: asks for topic and runs the full LangGraph pipeline
    """

    # Check if user wants to generate the diagram
    if "--diagram" in sys.argv:
        print("\n[INFO] Generating LangGraph Workflow Diagram...")
        path = save_workflow_diagram()
        if path:
            print(f"\n[OK] Diagram saved to: {path}")
        else:
            print("\nℹ️  PNG diagram not saved, but Mermaid text printed above.")
        return

    # ── Interactive Terminal Mode ──────────────────────────────────────────────
    print("\n" + "═" * 60)
    print("  🤖 LangGraph Blog Generator — Terminal Demo")
    print("═" * 60)
    print("\nThis demo shows how 4 AI agents work together using LangGraph.")
    print("Each agent modifies a shared state object and passes it to the next.\n")

    # Ask user for a blog topic
    print("Enter a blog topic to generate a blog post about.")
    print("Example: 'Machine Learning for Beginners', 'The Future of AI'\n")

    try:
        topic = input("📝 Enter blog topic: ").strip()
    except KeyboardInterrupt:
        print("\n\nExiting demo. Goodbye!")
        sys.exit(0)

    # Validate input
    if not topic:
        print("❌ No topic entered. Please run the script again and enter a topic.")
        sys.exit(1)

    print(f"\n[OK] Topic received: '{topic}'")
    print("Starting LangGraph workflow...\n")

    # Run the complete LangGraph workflow
    # This executes all 4 agents in sequence:
    #   planner → writer → editor → seo
    try:
        final_state = run_workflow(topic)
    except EnvironmentError as e:
        # This is the "no API key found" error from llm_provider.py
        print(e)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during workflow: {e}")
        raise

    # ── Print Full Results ─────────────────────────────────────────────────────
    print("\n" + "═" * 60)
    print("  📄 FULL BLOG GENERATION RESULTS")
    print("═" * 60)

    log_section("BLOG OUTLINE", final_state.get("outline", "N/A"))
    log_section("DRAFT BLOG (raw)", final_state.get("draft_blog", "N/A"))
    log_section("EDITED BLOG (polished)", final_state.get("edited_blog", "N/A"))
    log_section("SEO TITLE", final_state.get("seo_title", "N/A"))
    log_section("META DESCRIPTION", final_state.get("meta_description", "N/A"))

    # ── Summary Stats ──────────────────────────────────────────────────────────
    print("\n" + "─" * 60)
    print("Summary:")
    print(f"  Topic          : {final_state.get('topic', '')}")
    print(f"  SEO Title      : {final_state.get('seo_title', '')} ({len(final_state.get('seo_title', ''))} chars)")
    print(f"  Meta Desc Len  : {len(final_state.get('meta_description', ''))} chars")
    print(f"  Blog Word Count: ~{len(final_state.get('edited_blog', '').split())} words")
    print("─" * 60)

    print("\nTip: Run `streamlit run app/streamlit_app.py` to see this in a web UI!")
    print("Tip: Run `python run_demo.py --diagram` to visualize the workflow graph.\n")


if __name__ == "__main__":
    main()
