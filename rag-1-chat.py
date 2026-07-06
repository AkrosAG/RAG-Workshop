"""Stage 1 — Backbone: connect to a model and send one prompt.

No RAG yet. This is the foundation every later script builds on:
an OpenAI-compatible client (Ollama by default, any LiteLLM proxy via .env)
and a single chat completion.

Run:  poetry run python rag-1-chat.py "Why is the sky blue?"
"""

import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# --- Configuration (shared by all stages) ---
CHAT_MODEL = os.getenv("LLM_MODEL", "llama3.2")
client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
    api_key=os.getenv("LLM_API_KEY", "ollama"),
)

# --- Ask ---
question = " ".join(sys.argv[1:]) or "Say hello in one short sentence."

answer = client.chat.completions.create(
    model=CHAT_MODEL,
    messages=[{"role": "user", "content": question}],
)

print(answer.choices[0].message.content)
