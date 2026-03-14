"""
app/streamlit_app.py — Streamlit Web UI for the LangGraph Blog Generator
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from graph.workflow import run_workflow

# ── Page config — must be the very first Streamlit call ────────────────────────
st.set_page_config(
    page_title="LangGraph Blog Generator",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global dark-theme CSS (OpenAI-style) ───────────────────────────────────────
st.markdown("""
<style>
/* ── Base & background ───────────────────────── */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #0a0a0a !important;
    color: #e8e8e8;
}
[data-testid="stHeader"] { background-color: #0a0a0a !important; }

/* ── Sidebar ─────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #0f0f0f !important;
    border-right: 1px solid #1e1e1e !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] li { color: #9a9a9a !important; font-size: 13px !important; }
[data-testid="stSidebar"] h1 { color: #ffffff !important; font-size: 16px !important; font-weight: 700 !important; }
[data-testid="stSidebar"] h3 { color: #cccccc !important; font-size: 13px !important; font-weight: 600 !important; letter-spacing: 0.06em; text-transform: uppercase; margin-top: 1.2rem !important; }
[data-testid="stSidebar"] a { color: #777 !important; }
[data-testid="stSidebarUserContent"] { padding-top: 1.6rem; }

/* ── Main content ────────────────────────────── */
.block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 860px !important;
}

/* ── Typography ──────────────────────────────── */
h1 { color: #ffffff !important; font-weight: 700 !important; font-size: 2rem !important; letter-spacing: -0.02em; }
h2, h3 { color: #e0e0e0 !important; font-weight: 600 !important; }
p, li { color: #9a9a9a !important; line-height: 1.7; }
label { color: #cccccc !important; font-size: 13px !important; font-weight: 500 !important; }

/* ── Input fields ────────────────────────────── */
.stTextInput input {
    background-color: #141414 !important;
    border: 1px solid #2a2a2a !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
    transition: border-color 0.2s;
}
.stTextInput input:focus {
    border-color: #444 !important;
    box-shadow: none !important;
}
.stTextInput input::placeholder { color: #444 !important; }

/* ── Select box ──────────────────────────────── */
.stSelectbox > div > div {
    background-color: #141414 !important;
    border: 1px solid #2a2a2a !important;
    color: #cccccc !important;
    border-radius: 8px !important;
}

/* ── Primary button ──────────────────────────── */
button[kind="primary"], .stButton > button[kind="primary"] {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 20px !important;
    letter-spacing: 0.01em;
    transition: background-color 0.15s !important;
}
button[kind="primary"]:hover { background-color: #dedede !important; }

/* ── Secondary / regular buttons ─────────────── */
.stButton > button {
    background-color: #141414 !important;
    color: #cccccc !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    transition: border-color 0.15s !important;
}
.stButton > button:hover { border-color: #444 !important; }

/* ── Expander ────────────────────────────────── */
[data-testid="stExpander"] {
    background-color: #111111 !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 10px !important;
    overflow: hidden;
}
[data-testid="stExpander"] summary {
    color: #cccccc !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 14px 16px !important;
}
[data-testid="stExpander"] summary:hover { background-color: #161616 !important; }
[data-testid="stExpander"] > div > div { padding: 0 16px 16px 16px; }

/* ── Success / info / warning boxes ──────────── */
[data-testid="stSuccess"] {
    background-color: #0c1a0c !important;
    border: 1px solid #1a3a1a !important;
    border-radius: 8px !important;
    color: #7ec87e !important;
}
[data-testid="stInfo"] {
    background-color: #0c1520 !important;
    border: 1px solid #1a3050 !important;
    border-radius: 8px !important;
    color: #7eb8d4 !important;
}

/* ── Divider ─────────────────────────────────── */
hr { border-color: #1e1e1e !important; margin: 1.5rem 0 !important; }

/* ── Spinner ─────────────────────────────────── */
.stSpinner > div { border-top-color: #666 !important; }

/* ── JSON viewer ─────────────────────────────── */
.stJson > div {
    background-color: #111 !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 8px !important;
}

/* ── Download button ─────────────────────────── */
.stDownloadButton > button {
    background-color: #141414 !important;
    color: #cccccc !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 8px !important;
    font-size: 13px !important;
}

/* ── Caption ─────────────────────────────────── */
.stCaption, small { color: #444 !important; font-size: 12px !important; }

/* ── Custom components ───────────────────────── */
.pill {
    display: inline-block;
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 11px;
    color: #666;
    margin-bottom: 6px;
    letter-spacing: 0.04em;
}
.result-card {
    background: #111111;
    border: 1px solid #1e1e1e;
    border-radius: 12px;
    padding: 20px 22px;
    margin-bottom: 12px;
}
.result-card-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #555;
    margin-bottom: 8px;
}
.result-card-value {
    font-size: 17px;
    font-weight: 600;
    color: #f0f0f0;
    line-height: 1.4;
}
.result-card-sub {
    font-size: 13px;
    color: #9a9a9a;
    line-height: 1.6;
    margin-top: 6px;
}
.char-ok  { font-size: 11px; color: #4a9a4a; margin-top: 4px; }
.char-bad { font-size: 11px; color: #a04a4a; margin-top: 4px; }
.pipeline-step {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 10px;
}
.step-num {
    width: 22px; height: 22px;
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 700; color: #888;
    flex-shrink: 0; margin-top: 1px;
}
.step-body { flex: 1; }
.step-title { font-size: 13px; font-weight: 600; color: #cccccc; }
.step-desc  { font-size: 12px; color: #555; margin-top: 1px; }
.concept-row { margin-bottom: 8px; }
.concept-key { font-size: 12px; font-weight: 600; color: #999; }
.concept-val { font-size: 12px; color: #555; margin-top: 1px; }
.sidebar-divider { border: none; border-top: 1px solid #1e1e1e; margin: 14px 0; }
.badge-groq {
    background: #141414;
    border: 1px solid #2a2a2a;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
    color: #666;
}
</style>
""", unsafe_allow_html=True)


# ── SIDEBAR ─────────────────────────────────────────────────────────────────────
with st.sidebar:

    st.markdown("<h1>LangGraph</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#444;font-size:12px;margin-top:-8px;'>Agentic AI • Blog Generator</p>", unsafe_allow_html=True)

    st.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)

    # Agent pipeline steps
    st.markdown("<h3>Agent Pipeline</h3>", unsafe_allow_html=True)
    steps = [
        ("Planner Agent",  "Topic → structured outline"),
        ("Writer Agent",   "Outline → draft blog post"),
        ("Editor Agent",   "Draft → polished writing"),
        ("SEO Agent",      "Blog → title + meta desc"),
    ]
    for i, (title, desc) in enumerate(steps, 1):
        st.markdown(f"""
        <div class="pipeline-step">
            <div class="step-num">{i}</div>
            <div class="step-body">
                <div class="step-title">{title}</div>
                <div class="step-desc">{desc}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)

    # LangGraph core concepts
    st.markdown("<h3>Core Concepts</h3>", unsafe_allow_html=True)
    concepts = [
        ("State",  "Shared data object that every agent reads and writes"),
        ("Node",   "A single agent function in the graph"),
        ("Edge",   "The connection that defines execution order"),
        ("Graph",  "The compiled pipeline of all nodes + edges"),
    ]
    for key, val in concepts:
        st.markdown(f"""
        <div class="concept-row">
            <div class="concept-key">{key}</div>
            <div class="concept-val">{val}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)

    # Model info
    st.markdown("<h3>Model</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class="badge-groq">
        Groq &nbsp;·&nbsp; llama-3.3-70b-versatile<br>
        <span style='color:#444;font-size:11px;'>Free tier · ~1s response</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:11px;color:#333;'>Built with LangGraph + Streamlit</p>", unsafe_allow_html=True)


# ── HERO SECTION ────────────────────────────────────────────────────────────────
st.markdown("""
<div style='margin-bottom: 2rem;'>
    <div style='font-size:11px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#555;margin-bottom:10px;'>Agentic AI</div>
    <h1 style='margin:0 0 10px 0;'>Blog Generator</h1>
    <p style='font-size:15px;color:#555;max-width:600px;line-height:1.6;margin:0;'>
        Enter any topic. Four specialized AI agents collaborate in a LangGraph pipeline
        to produce a complete, SEO-optimized blog post.
    </p>
</div>
""", unsafe_allow_html=True)


st.markdown("<hr>", unsafe_allow_html=True)


# ── INPUT ────────────────────────────────────────────────────────────────────────
st.markdown("<h2 style='font-size:18px;font-weight:600;margin-bottom:16px;'>Enter a topic</h2>", unsafe_allow_html=True)

example_topics = [
    "Select an example...",
    "Machine Learning for Beginners",
    "The Future of Electric Vehicles",
    "Why Python is Great for Data Science",
    "Benefits of Remote Work",
    "Introduction to Blockchain Technology",
]

col_input, col_example = st.columns([2, 1])
with col_input:
    topic = st.text_input(
        "Blog Topic",
        placeholder="e.g., 'The Future of Quantum Computing'",
        label_visibility="collapsed",
    )
with col_example:
    selected = st.selectbox("Example", example_topics, label_visibility="collapsed")
    if selected != "Select an example...":
        topic = selected

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

generate_btn = st.button(
    "Generate Blog",
    type="primary",
    use_container_width=True,
    disabled=not bool(topic and topic.strip()),
)


# ── WORKFLOW EXECUTION ───────────────────────────────────────────────────────────
if generate_btn and topic and topic.strip():
    with st.spinner("Running pipeline — watch your terminal for live agent logs..."):
        try:
            result = run_workflow(topic.strip())
            st.session_state["result"] = result
            st.session_state["topic"] = topic.strip()
        except EnvironmentError as e:
            st.error(str(e))
            st.stop()
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.exception(e)
            st.stop()


# ── RESULTS ──────────────────────────────────────────────────────────────────────
if "result" in st.session_state:
    result    = st.session_state["result"]
    topic_used = st.session_state.get("topic", "")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='display:flex;align-items:center;gap:10px;margin-bottom:1.5rem;'>
        <div style='width:8px;height:8px;background:#3a7a3a;border-radius:50%;'></div>
        <span style='font-size:13px;color:#666;'>Generated for: <strong style='color:#aaa;'>{topic_used}</strong></span>
    </div>
    """, unsafe_allow_html=True)

    # ── SEO cards ──────────────────────────────────────────────────────────────
    st.markdown("<h2 style='font-size:18px;font-weight:600;margin-bottom:14px;'>SEO Metadata</h2>", unsafe_allow_html=True)

    seo_col1, seo_col2 = st.columns(2)

    with seo_col1:
        seo_title = result.get("seo_title", "")
        char_t = len(seo_title)
        char_class = "char-ok" if char_t <= 60 else "char-bad"
        st.markdown(f"""
        <div class="result-card">
            <div class="result-card-label">SEO Title &nbsp;·&nbsp; Agent 4</div>
            <div class="result-card-value">{seo_title or "—"}</div>
            <div class="{char_class}">{char_t} / 60 characters</div>
        </div>""", unsafe_allow_html=True)

    with seo_col2:
        meta = result.get("meta_description", "")
        char_m = len(meta)
        char_class2 = "char-ok" if char_m <= 150 else "char-bad"
        st.markdown(f"""
        <div class="result-card">
            <div class="result-card-label">Meta Description &nbsp;·&nbsp; Agent 4</div>
            <div class="result-card-sub">{meta or "—"}</div>
            <div class="{char_class2}">{char_m} / 150 characters</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Blog content expanders ─────────────────────────────────────────────────
    st.markdown("<h2 style='font-size:18px;font-weight:600;margin-bottom:14px;'>Blog Content</h2>", unsafe_allow_html=True)

    with st.expander("Outline  —  Agent 1: Planner", expanded=True):
        st.markdown(f"<div class='pill'>planner_agent.py &nbsp;·&nbsp; reads: topic &nbsp;·&nbsp; writes: outline</div>", unsafe_allow_html=True)
        st.markdown(result.get("outline") or "_No outline generated._")

    with st.expander("Draft  —  Agent 2: Writer", expanded=False):
        st.markdown(f"<div class='pill'>writer_agent.py &nbsp;·&nbsp; reads: topic + outline &nbsp;·&nbsp; writes: draft_blog</div>", unsafe_allow_html=True)
        st.markdown(result.get("draft_blog") or "_No draft generated._")

    with st.expander("Final Blog  —  Agent 3: Editor", expanded=True):
        st.markdown(f"<div class='pill'>editor_agent.py &nbsp;·&nbsp; reads: draft_blog &nbsp;·&nbsp; writes: edited_blog</div>", unsafe_allow_html=True)
        edited = result.get("edited_blog", "")
        st.markdown(edited or "_No edited blog generated._")
        if edited:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.download_button(
                label="Download Blog Post",
                data=edited,
                file_name=f"blog_{topic_used[:30].replace(' ', '_')}.txt",
                mime="text/plain",
            )

    # ── LangGraph state inspector ──────────────────────────────────────────────
    with st.expander("LangGraph State Inspector", expanded=False):
        st.markdown("""
        <div style='font-size:13px;color:#555;margin-bottom:12px;line-height:1.6;'>
            This is the complete <strong style='color:#777'>BlogState</strong> object after all 4 agents have finished.
            Each key was written by a different agent — this is how state flows through a LangGraph pipeline.
        </div>""", unsafe_allow_html=True)
        st.json({
            "topic":            result.get("topic", ""),
            "outline":          (result.get("outline", "") or "")[:200] + "...",
            "draft_blog":       (result.get("draft_blog", "") or "")[:200] + "...",
            "edited_blog":      (result.get("edited_blog", "") or "")[:200] + "...",
            "seo_title":        result.get("seo_title", ""),
            "meta_description": result.get("meta_description", ""),
        })


# ── FOOTER ───────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center;padding:8px 0 4px;'>
    <span style='font-size:12px;color:#2a2a2a;letter-spacing:0.04em;'>
        LangGraph &nbsp;·&nbsp; Streamlit &nbsp;·&nbsp; Groq &nbsp;·&nbsp; LLaMA 3.3
    </span>
</div>""", unsafe_allow_html=True)
