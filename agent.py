"""
agent.py

The smallest possible Agent:

    input (str)
        |
        v
    messages (list[dict])
        |
        v
    model.complete(messages)
        |
        v
    output (str)

Agent deliberately knows nothing about OpenAI, environment variables,
or HTTP. It only knows the ChatModel *shape* from model.py. This is
dependency inversion in the smallest form we can show it: Agent depends
on an abstraction (ChatModel), not on a concrete provider (OpenAIModel).

That means: a FakeModel that returns canned strings can be swapped in
here with zero changes to this file — which is exactly what we'll do
when we write tests in a later lesson.
"""

from __future__ import annotations

from model import ChatModel


class Agent:
    def __init__(self, model: ChatModel) -> None:
        self.model = model

    async def run(self, prompt: str) -> str:
        # Step 1: turn the raw string into the shape the model expects.
        # Right now this is a single user message. Stage 2 of the
        # broader roadmap will replace plain dicts with real Message
        # types — but the *shape* of this list won't fundamentally change.
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]

        # Step 2: delegate to the model. Agent does not know or care
        # whether this hits a real API, a cache, or a test double.
        return await self.model.complete(messages)
