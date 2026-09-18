"""
main.py

The runnable entrypoint. Wires the concrete GroqModel into the
provider-agnostic Agent, runs one prompt, prints the result.

Execution flow:

    main()
      |
      v
    Agent.run(prompt)
      |
      v
    messages = [...]
      |
      v
    model.complete(messages)
      |
      v
    Groq API (OpenAI-compatible)
      |
      v
    response (str)
      |
      v
    Agent.run() returns
      |
      v
    main() prints it
"""

from __future__ import annotations

import asyncio

from agent import Agent
from model import GroqModel


async def main() -> None:
    model = GroqModel()  # reads GROQ_API_KEY from .env, free tier
    agent = Agent(model)

    response = await agent.run(
        "Explain what an AI agent is in three sentences."
    )

    print(response)


if __name__ == "__main__":
    asyncio.run(main())
