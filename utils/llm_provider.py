"""
utils/llm_provider.py — LLM Provider Utility

PURPOSE:
--------
This module is the "brain supplier" for all agents.
Instead of hardcoding which LLM to use in each agent, we centralize the choice here.

REAL-LIFE ANALOGY:
------------------
Think of this like a staffing agency. Every agent in your team says:
  "Give me a smart assistant to talk to."
This module checks your credentials and hands them the best available assistant.

FREE API KEY PRIORITY:
----------------------
  1. If GROQ_API_KEY is set      → use llama-3.3-70b-versatile  ✅ TRULY FREE
  2. If OPENAI_API_KEY is set    → use gpt-4o-mini               (requires credits)
  3. If ANTHROPIC_API_KEY is set → use claude-3-haiku             (requires credits)
  4. None found                  → raise a clear error

WHY GROQ IS BEST FOR DEMOS:
----------------------------
  - Groq provides a 100% free tier (no credit card required)
  - It runs open-source LLaMA 3 models on custom hardware (LPU chips)
  - Speed is 10x faster than OpenAI — responses arrive in <1 second
  - Free tier limits: ~30 requests/minute, ~6000 tokens/minute (plenty for demos)
  - Get a free key at: https://console.groq.com/keys

REAL-LIFE ANALOGY FOR GROQ:
----------------------------
  Groq is like a free, super-fast sports car for AI inference.
  OpenAI/Anthropic are like taxis — great quality but you pay per ride.
  For a demo, the free sports car is the obvious choice!
"""

import os
from dotenv import load_dotenv

# Load environment variables from the .env file in the project root
# This lets users simply add their key to .env without touching code
load_dotenv()


def get_llm():
    """
    Returns the best available LLM based on environment variables.

    Priority order:
        1. GROQ_API_KEY      → llama-3.3-70b-versatile (FREE, fast, great quality)
        2. OPENAI_API_KEY    → gpt-4o-mini (paid, reliable)
        3. ANTHROPIC_API_KEY → claude-3-haiku (paid, reliable)

    Returns:
        A LangChain chat model instance (ChatGroq, ChatOpenAI, or ChatAnthropic)

    Raises:
        EnvironmentError: If no API key is configured

    Usage example:
        llm = get_llm()
        response = llm.invoke("Write a short poem about Python.")
    """

    groq_key = os.getenv("GROQ_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    # --- Option 1: Groq (RECOMMENDED — Truly Free) ---
    # Groq runs LLaMA 3.3 70B on custom LPU hardware — blazing fast and free.
    # llama-3.3-70b-versatile is a top-tier open-source model.
    # Free tier: ~30 RPM, ~6000 TPM — more than enough for this demo.
    # Get key at: https://console.groq.com/keys
    if groq_key and groq_key.strip():
        from langchain_groq import ChatGroq
        print("[OK] LLM Provider: Groq (llama-3.3-70b-versatile) - FREE TIER")
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=groq_key,
            max_tokens=500,      # Keep outputs short to stay within free limits
            temperature=0.7,     # Slightly creative but not too random
        )

    # --- Option 2: OpenAI GPT-4o-mini (requires paid credits) ---
    # gpt-4o-mini is the cheapest OpenAI model.
    # Input: ~$0.15 / 1M tokens | Output: ~$0.60 / 1M tokens
    if openai_key and openai_key.strip():
        from langchain_openai import ChatOpenAI
        print("[OK] LLM Provider: OpenAI (gpt-4o-mini)")
        return ChatOpenAI(
            model="gpt-4o-mini",
            api_key=openai_key,
            max_tokens=500,
            temperature=0.7,
        )

    # --- Option 3: Anthropic Claude 3 Haiku (requires paid credits) ---
    # claude-3-haiku is Anthropic's fastest and cheapest model.
    # Input: ~$0.25 / 1M tokens | Output: ~$1.25 / 1M tokens
    if anthropic_key and anthropic_key.strip():
        from langchain_anthropic import ChatAnthropic
        print("[OK] LLM Provider: Anthropic (claude-3-haiku-20240307)")
        return ChatAnthropic(
            model="claude-3-haiku-20240307",
            api_key=anthropic_key,
            max_tokens=500,
            temperature=0.7,
        )

    # --- No API key found ---
    raise EnvironmentError(
        "\n\n❌ ERROR: No LLM API key found!\n"
        "Please add one of the following to your .env file:\n\n"
        "  GROQ_API_KEY=gsk_...        ← RECOMMENDED (100%% free)\n"
        "                                 Get key at: https://console.groq.com/keys\n\n"
        "  OPENAI_API_KEY=sk-...       ← requires paid credits\n"
        "  ANTHROPIC_API_KEY=sk-ant-... ← requires paid credits\n\n"
        "Copy .env.example to .env and fill in your key.\n"
    )
