# 🤖 LangGraph Blog Generator — Agentic AI Demo

A **hands-on demonstration of Agentic AI** using [LangGraph](https://langchain-ai.github.io/langgraph/).

This project shows how multiple AI agents can collaborate as a team, each handling a specialized task, with a shared state flowing through them — just like a real content production pipeline.

---

## 🧠 What Is Agentic AI?

Traditional AI: You ask → AI answers → Done.

**Agentic AI**: A *team* of specialized AI agents works together on a task:
- Each agent has a specific role
- They pass information to the next agent
- The final output is the result of collaboration

**Real-life analogy**: Like a blog publishing team:
| Person | Role |
|--------|------|
| Senior Editor | Plans the structure |
| Journalist | Writes the content |
| Copy Editor | Polishes the text |
| SEO Specialist | Adds search optimization |

In this demo, each of those roles is an AI agent!

---

## 🔄 How LangGraph Works

LangGraph uses three core concepts:

| Concept | What it is | Real-life analogy |
|---------|-----------|-------------------|
| **State** | Shared data object passed between agents | A form being filled out by multiple people |
| **Node** | An individual agent (Python function) | A worker at a station on an assembly line |
| **Edge** | A connection between two nodes | The conveyor belt between stations |

### Workflow Diagram

```
START
  │
  ▼
[Planner Agent]  ─── reads: topic        │ writes: outline
  │
  ▼
[Writer Agent]   ─── reads: topic+outline │ writes: draft_blog
  │
  ▼
[Editor Agent]   ─── reads: draft_blog    │ writes: edited_blog
  │
  ▼
[SEO Agent]      ─── reads: edited_blog   │ writes: seo_title + meta_description
  │
  ▼
END
```

---

## 📁 Project Structure

```
agentic_demo/
├── agents/
│   ├── planner_agent.py     # Agent 1: Creates blog outline
│   ├── writer_agent.py      # Agent 2: Writes the draft blog
│   ├── editor_agent.py      # Agent 3: Edits and polishes
│   └── seo_agent.py         # Agent 4: Generates SEO metadata
│
├── graph/
│   ├── state.py             # Shared state definition (BlogState TypedDict)
│   └── workflow.py          # LangGraph StateGraph — nodes + edges
│
├── utils/
│   ├── llm_provider.py      # LLM selector (OpenAI or Anthropic)
│   └── logger.py            # Terminal logging helpers
│
├── app/
│   └── streamlit_app.py     # Streamlit web UI
│
├── run_demo.py              # Terminal runner (no UI needed)
├── requirements.txt         # Python dependencies
├── .env.example             # Template for API keys
└── README.md                # This file
```

---

## ⚡ Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Up Your API Key

```bash
# Copy the example file
cp .env.example .env

# Open .env and add your key:
# OPENAI_API_KEY=sk-...   (get free key at platform.openai.com)
# OR
# ANTHROPIC_API_KEY=sk-... (get free key at console.anthropic.com)
```

> **Note:** You only need ONE key. The system will automatically pick the right model.

### Step 3: Run the Streamlit App

```bash
streamlit run app/streamlit_app.py
```

Then open your browser to `http://localhost:8501`

---

## 🖥️ Terminal Mode (No Browser Needed)

You can also run the demo entirely in the terminal:

```bash
# Run the full pipeline interactively
python run_demo.py

# Generate the workflow visualization diagram
python run_demo.py --diagram
```

---

## 🤖 Agents Explained

### Agent 1: Content Planner
- **Input:** topic (from user)
- **Output:** `outline` — a 3–5 section blog structure
- **Like:** A journalist outlining their article before writing

### Agent 2: Writer
- **Input:** topic + outline
- **Output:** `draft_blog` — a short 3–5 paragraph blog post
- **Like:** A journalist writing the first draft

### Agent 3: Editor
- **Input:** draft_blog
- **Output:** `edited_blog` — polished, grammar-corrected version
- **Like:** A copy editor refining the journalist's draft

### Agent 4: SEO Optimizer
- **Input:** edited_blog
- **Output:** `seo_title` (max 60 chars) + `meta_description` (max 150 chars)
- **Like:** An SEO specialist writing the Google search snippet

---

## 💰 Cost Optimization

This demo is designed for **free tier API keys**:

| Model | Provider | Cost (approximate) |
|-------|----------|-------------------|
| `gpt-4o-mini` | OpenAI | ~$0.001 per blog |
| `claude-3-haiku` | Anthropic | ~$0.002 per blog |

Each run generates a blog of ~200-250 words using ~500-800 total tokens.

---

## 🔑 Key LangGraph Concepts Demonstrated

1. **StateGraph** — The main graph class that holds all nodes and edges
2. **TypedDict State** — A typed Python dict that defines the shared state schema
3. **Node functions** — Python functions that accept state and return partial updates
4. **Sequential edges** — Simple linear pipeline (no branching in this demo)
5. **START / END** — Special LangGraph constants for workflow entry and exit points
6. **graph.compile()** — Validates and builds the runnable workflow object
7. **graph.invoke()** — Executes the full workflow and returns the final state

---

## 📚 Learn More

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph Tutorials](https://langchain-ai.github.io/langgraph/tutorials/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [Anthropic API Keys](https://console.anthropic.com/)

---

*Built as a teaching/demo project to explain Agentic AI concepts to teams new to LLMs.*
