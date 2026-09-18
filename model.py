"""
model.py

Responsibility of this file — and ONLY this file:

    messages (list[dict])
        |
        v
    API request to the LLM provider
        |
        v
    text response (str)

This module knows nothing about "agents", "tools", or "prompts" in the
agent-framework sense. It knows how to turn a list of chat messages into
a string reply from a model. That's the entire contract.

Why a Protocol?
----------------
`ChatModel` below is not a class you instantiate — it's a *shape*.
Anything with an async `complete(messages) -> str` method satisfies it,
without inheriting from anything. This means `agent.py` can depend on
`ChatModel` instead of depending on `OpenAIModel` directly. Later, when
we add a `FakeModel` for tests, or a second provider, `agent.py` will
not need to change at all — that's the whole point of the abstraction.
"""

from __future__ import annotations

import os
from typing import Protocol

from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load variables from a local .env file (e.g. OPENAI_API_KEY=...) into
# the process environment. This only affects THIS process, not your
# actual shell/OS environment.
load_dotenv()


class ChatModel(Protocol):
    """The minimal shape an Agent needs from a model.

    Any class with this async method can be used by Agent — real API,
    fake test double, local model, doesn't matter.
    """

    async def complete(self, messages: list[dict[str, str]]) -> str:
        ...


class OpenAIModel:
    """A ChatModel implementation backed by the real OpenAI API.

    This class does exactly one job: given chat messages, return the
    model's text reply. It does not retry, does not stream, does not
    know what a "tool" is. Those are later lessons.
    """

    def __init__(self, model: str = "gpt-4o-mini", api_key: str | None = None) -> None:
        # Prefer an explicitly passed key, otherwise fall back to the
        # OPENAI_API_KEY environment variable (populated by load_dotenv()
        # above, or set some other way).
        resolved_key = api_key or os.getenv("OPENAI_API_KEY")
        if not resolved_key:
            raise RuntimeError(
                "No OpenAI API key found. Set OPENAI_API_KEY in a .env "
                "file (see .env.example) or pass api_key= explicitly."
            )

        self._client = AsyncOpenAI(api_key=resolved_key)
        self._model = model

    async def complete(self, messages: list[dict[str, str]]) -> str:
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=messages,  # type: ignore[arg-type]
        )
        content = response.choices[0].message.content
        return content or ""


class GroqModel:
    """A ChatModel implementation backed by Groq's free-tier API.

    Groq exposes an OpenAI-compatible endpoint, so we reuse the same
    `openai` SDK we already have installed — we just point it at a
    different `base_url` and use a Groq API key instead of an OpenAI
    one. This is the payoff of the ChatModel abstraction: swapping
    providers is a new class, not a rewrite of Agent or main.py.

    Get a free key (no credit card) at https://console.groq.com/keys
    """

    def __init__(
        self,
        model="openai/gpt-oss-20b",
        api_key: str | None = None,
    ) -> None:
        resolved_key = api_key or os.getenv("GROQ_API_KEY")
        if not resolved_key:
            raise RuntimeError(
                "No Groq API key found. Set GROQ_API_KEY in a .env file "
                "(see .env.example) or pass api_key= explicitly. Get a "
                "free key at https://console.groq.com/keys"
            )

        self._client = AsyncOpenAI(
            api_key=resolved_key,
            base_url="https://api.groq.com/openai/v1",
        )
        self._model = model

    async def complete(self, messages: list[dict[str, str]]) -> str:
        """Send messages to the OpenAI Chat Completions API, return text.

        messages looks like:
            [{"role": "user", "content": "Explain X"}]

        We return only the text of the first choice's message content.
        Everything else the API gives back (usage, finish_reason, etc.)
        is discarded here on purpose — this file's contract is just
        "messages in, text out".
        """
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=messages,  # type: ignore[arg-type]
        )
        content = response.choices[0].message.content
        return content or ""
