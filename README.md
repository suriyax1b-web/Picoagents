# picoagents

A tiny, from-scratch agent skeleton: `Agent` → `ChatModel` → LLM API → response.

Currently wired to **Groq's free tier** (no credit card required, OpenAI-compatible API).

```text
main.py
  │
  ▼
Agent.run(prompt)
  │
  ▼
messages = [{"role": "user", "content": prompt}]
  │
  ▼
model.complete(messages)   ← GroqModel, defined in model.py
  │
  ▼
Groq API (OpenAI-compatible)
  │
  ▼
response (str)
  │
  ▼
print(response)
```

## Files

| File | Purpose |
|---|---|
| `main.py` | Entry point. Wires `GroqModel` into `Agent`, runs one prompt. |
| `agent.py` | `Agent` class — knows nothing about any specific provider. |
| `model.py` | `ChatModel` protocol + `GroqModel` (active) + `OpenAIModel` (kept for reference — swap back by importing it in `main.py` and setting `OPENAI_API_KEY` in `.env`). |
| `requirements.txt` | `openai` (used for both Groq and OpenAI — Groq is OpenAI-compatible) + `python-dotenv`. |
| `.env` | Your real API key goes here. Never commit this. |
| `.env.example` | Template showing what `.env` should contain. |
| `.gitignore` | Excludes `.env`, virtual envs, and Python cache files from git. |

## 1. Install dependencies

```bash
python -m venv .venv
```

Activate it:
- macOS/Linux: `source .venv/bin/activate`
- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- Windows cmd.exe: `.venv\Scripts\activate.bat`

Then:

```bash
pip install -r requirements.txt
```

## 2. Configure environment variables

Get a free API key (no credit card) at **https://console.groq.com/keys**.

Open `.env` and replace the placeholder:

```text
GROQ_API_KEY=your_key_here
```

with your real key.

## 3. Run it

```bash
python main.py
```

Entry point / main command: **`python main.py`**

You should see a short response printed to the terminal within about a second — Groq's inference is unusually fast.

## Troubleshooting

- `ModuleNotFoundError: No module named 'openai'` → venv not activated, or VS Code is using a different Python interpreter than your terminal (Command Palette → "Python: Select Interpreter" → pick the one inside `.venv`).
- `RuntimeError: No Groq API key found` → `.env` still has the placeholder, or you're running from a different working directory than where `.env` lives.
- `AuthenticationError` → key was copied incorrectly (extra space, truncated, or revoked).

## Switching back to OpenAI

`OpenAIModel` is still defined in `model.py`. To use it instead:

1. In `main.py`, change `from model import GroqModel` to `from model import OpenAIModel`, and `model = GroqModel()` to `model = OpenAIModel()`.
2. In `.env`, add `OPENAI_API_KEY=your_key_here` (Groq's line can stay or go).

No changes to `agent.py` are ever needed — that's the point of the `ChatModel` abstraction.
