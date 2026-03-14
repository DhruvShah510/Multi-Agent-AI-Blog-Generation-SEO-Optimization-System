# 🤖 Multi-Agent AI Blog Generation & SEO Optimization System

A **LangGraph-based multi-agent AI system** that automatically generates structured blog content using a collaborative pipeline of specialized AI agents.

This project demonstrates how **agentic AI architectures** can orchestrate multiple Large Language Model (LLM) agents to perform complex workflows such as **content planning, drafting, editing, and SEO optimization**.

Instead of relying on a single LLM prompt, the system uses a **coordinated agent pipeline** where each agent focuses on a specific responsibility, resulting in higher quality and more structured outputs.

---

# 🧠 Project Overview

The system simulates a **real-world content production pipeline** using AI agents.

Each agent performs a specialized role:

| Agent | Responsibility |
|------|----------------|
| **Planner Agent** | Generates a structured outline from the topic |
| **Writer Agent** | Expands the outline into a draft blog |
| **Editor Agent** | Refines the draft for clarity and readability |
| **SEO Agent** | Generates an SEO title and meta description |

These agents collaborate through a **shared state managed by LangGraph**, enabling a structured and deterministic AI workflow.

---

# 🏗 Architecture

The system is implemented using **LangGraph's StateGraph architecture**, where agents operate as nodes connected through directed edges.

Key components:

| Component | Description |
|-----------|-------------|
| **State** | Shared data object passed between agents |
| **Nodes** | Individual AI agents implemented as Python functions |
| **Edges** | Connections defining the workflow order |

### Workflow Pipeline

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

This design demonstrates how **LLM-powered agents can be composed into modular pipelines for real-world AI applications.**

---

### ⚡ Key Features
- Multi-agent AI workflow using LangGraph
- Modular agent-based architecture
- Automated blog generation pipeline
- SEO metadata generation (title + description)
- Shared state management between agents
- Streamlit UI for interactive blog generation
- Terminal mode for quick testing

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

## ⚙️ Tech Stack & Concepts

### Technologies Used
- LangGraph
- LangChain
- OpenAI / Anthropic LLMs
- Python
- Streamlit
- Pydantic

### GenAI Concepts Demonstrated
This project showcases several important Generative AI system design patterns:

- Agentic AI workflows
- Multi-agent orchestration
- State-based LLM pipelines
- Prompt-driven agent collaboration
- Modular AI system design

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


# ⚡ Installation

### Step 1 :Clone the repository:

```bash
git clone https://github.com/DhruvShah510/Multi-Agent-AI-Blog-Generation-SEO-Optimization-System.git
cd Multi-Agent-AI-Blog-Generation-SEO-Optimization-System
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Your API Key

```bash
# Copy the example file
cp .env.example .env

# Open .env and add your key:
#GROQ_API_KEY = gsk-...   (get your free api key from groq api key platform)
# OPENAI_API_KEY=sk-...   (get paid key)
# OR
# ANTHROPIC_API_KEY=sk-... (get paid key)
```

> **Note:** You only need ONE key. The system will automatically pick the right model.

### Step 4: Run the Streamlit App

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

### Author 
Dhruv Shah

M.Tech – Computer Science & Engineering
Sardar Vallabhbhai National Institute of Technology (SVNIT)

---

### Contact 
LinkedIn
https://www.linkedin.com/in/dhruv-shah-25997624b

Email
dhruv.shahcs008@gmail.com

---

### ⭐ If you found this project interesting

Consider giving the repository a star ⭐

---