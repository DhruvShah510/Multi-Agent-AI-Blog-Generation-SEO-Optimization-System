"""
graph/workflow.py — LangGraph Workflow Definition

THIS IS THE CORE OF THE PROJECT — where LangGraph magic happens.

WHAT IS A LANGGRAPH WORKFLOW?
------------------------------
LangGraph lets you define AI pipelines as a GRAPH — with nodes and edges.

  - NODES  = individual agents (each is a Python function)
  - EDGES  = the connections that define execution order
  - STATE  = the shared data object passed through every node

REAL-LIFE ANALOGY:
------------------
Think of a production assembly line at a car factory:
  Station 1 (Planner) → adds the chassis
  Station 2 (Writer)  → adds the engine
  Station 3 (Editor)  → adds the paint
  Station 4 (SEO)     → adds final quality check

Each station receives the partially-built car, adds its part, and passes it on.
LangGraph is the conveyor belt that manages this flow.

WORKFLOW STRUCTURE:
-------------------
  START
    │
    ▼
  [planner]  ←── reads: topic         | writes: outline
    │
    ▼
  [writer]   ←── reads: topic+outline | writes: draft_blog
    │
    ▼
  [editor]   ←── reads: draft_blog    | writes: edited_blog
    │
    ▼
  [seo]      ←── reads: edited_blog   | writes: seo_title + meta_description
    │
    ▼
   END
"""

import os
from langgraph.graph import StateGraph, START, END
from graph.state import BlogState
from agents.planner_agent import planner_agent
from agents.writer_agent import writer_agent
from agents.editor_agent import editor_agent
from agents.seo_agent import seo_agent
from utils.logger import log_workflow_start, log_workflow_complete, log_section


def build_workflow():
    """
    Builds and compiles the LangGraph StateGraph.

    HOW IT WORKS:
    1. Create a StateGraph with our BlogState schema
    2. Add each agent as a "node" with a name
    3. Add "edges" to define the execution order
    4. Compile the graph into a runnable object

    Returns:
        A compiled LangGraph runnable (can be invoked with initial state)
    """

    # Step 1: Create the StateGraph
    # We pass BlogState so LangGraph knows the shape of our shared state.
    # This is like defining the columns of a spreadsheet before filling it in.
    graph = StateGraph(BlogState)

    # Step 2: Add nodes (agents)
    # Each node has:
    #   - a name (used in edges and logs)
    #   - a function (the agent that processes the state)
    #
    # The function must accept (state: BlogState) → dict
    graph.add_node("planner", planner_agent)   # Node 1: Creates the outline
    graph.add_node("writer", writer_agent)     # Node 2: Writes the draft
    graph.add_node("editor", editor_agent)     # Node 3: Edits the draft
    graph.add_node("seo", seo_agent)           # Node 4: Generates SEO metadata

    # Step 3: Add edges (define execution order)
    # Edges tell LangGraph which node runs after which.
    # START and END are special LangGraph constants for entry/exit points.
    #
    # This creates a LINEAR pipeline:
    #   START → planner → writer → editor → seo → END
    graph.add_edge(START, "planner")     # Workflow begins at planner
    graph.add_edge("planner", "writer")  # After planner finishes, run writer
    graph.add_edge("writer", "editor")   # After writer finishes, run editor
    graph.add_edge("editor", "seo")      # After editor finishes, run seo
    graph.add_edge("seo", END)           # After seo finishes, workflow ends

    # Step 4: Compile the graph
    # .compile() validates the graph structure and returns a runnable object.
    # Think of this like "building" the assembly line before starting production.
    compiled_graph = graph.compile()

    return compiled_graph


def run_workflow(topic: str) -> BlogState:
    """
    Runs the complete LangGraph workflow for a given blog topic.

    This is the main entry point used by both run_demo.py and streamlit_app.py.

    Args:
        topic: The blog topic the user wants to write about
               Example: "Python for Beginners"

    Returns:
        The final BlogState with all fields populated by the agents

    How it works:
        1. Build the compiled graph
        2. Create the initial state with just the topic
        3. Invoke the graph — LangGraph runs each node in order
        4. Return the final state after all 4 agents have run
    """

    log_workflow_start()

    # Build the LangGraph workflow
    app = build_workflow()

    # Create the initial state — only `topic` is set at the start.
    # All other fields (outline, draft_blog, etc.) start as empty strings.
    # Each agent will fill in its respective field as the workflow runs.
    initial_state = {
        "topic": topic,
        "outline": "",
        "draft_blog": "",
        "edited_blog": "",
        "seo_title": "",
        "meta_description": "",
    }

    # Run the entire LangGraph pipeline!
    # .invoke() executes all nodes in sequence and returns the final state.
    # Internally LangGraph:
    #   1. Passes initial_state to planner_agent
    #   2. Merges planner's output back into state
    #   3. Passes updated state to writer_agent
    #   4. Merges writer's output back into state
    #   5. ... and so on until all nodes are done
    final_state = app.invoke(initial_state)

    log_workflow_complete()

    # Print a summary of results in the terminal
    log_section("BLOG OUTLINE", final_state["outline"])
    log_section("SEO TITLE", final_state["seo_title"])
    log_section("META DESCRIPTION", final_state["meta_description"])

    return final_state


def save_workflow_diagram():
    """
    Generates and saves a visual diagram of the LangGraph workflow.

    Uses LangGraph's built-in Mermaid diagram generator.

    Mermaid is a text-based diagram language that can be rendered visually.
    The diagram shows all nodes and edges in the workflow.

    Output:
        - Prints the Mermaid diagram text to the terminal
        - Saves workflow_graph.png in the project root (if graphviz/PIL available)
    """

    print("\n[INFO] Generating workflow diagram...")

    app = build_workflow()

    # Get the Mermaid diagram as text
    # This shows the graph structure in a human-readable format
    mermaid_diagram = app.get_graph().draw_mermaid()

    print("\n--- Mermaid Diagram ---")
    print(mermaid_diagram)
    print("-----------------------\n")

    # Try to save as PNG image (requires additional libraries)
    # If not available, we just skip — the Mermaid text is still useful
    try:
        png_data = app.get_graph().draw_mermaid_png()
        diagram_path = os.path.join(os.path.dirname(__file__), "..", "workflow_graph.png")
        diagram_path = os.path.abspath(diagram_path)
        with open(diagram_path, "wb") as f:
            f.write(png_data)
        print(f"[OK] Workflow diagram saved to: {diagram_path}")
        return diagram_path
    except Exception as e:
        print(f"[INFO] Could not save PNG diagram: {e}")
        print("   (This is optional - the Mermaid text above shows the workflow structure)")
        return None
