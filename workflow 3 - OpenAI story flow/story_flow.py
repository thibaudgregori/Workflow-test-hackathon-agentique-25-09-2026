"""Exemple officiel OpenAI Agents SDK : examples/agent_patterns/deterministic.py
(openai/openai-agents-python @ 588826c, licence MIT, voir LICENSE-openai-agents).

Le code des agents et du flux est celui d'OpenAI. Seuls changements, marqués
« DEADWEIGHT » : la connexion (passerelle, API chat/completions, pas de traces
envoyées à OpenAI), le modèle choisi par variable d'environnement, la demande
passée en argument au lieu d'une saisie clavier, et `return` au lieu de `exit(0)`
pour pouvoir enchaîner plusieurs exécutions.

    python story_flow.py "Une histoire de science-fiction sur Mars"
"""
import asyncio
import os
import sys

from openai import AsyncOpenAI
from pydantic import BaseModel

from agents import (Agent, Runner, set_default_openai_api, set_default_openai_client,
                    set_tracing_disabled, trace)

# DEADWEIGHT : tous les appels passent par la passerelle, en chat/completions
# (la passerelle ne capte pas encore l'API Responses, défaut du SDK).
set_default_openai_client(AsyncOpenAI(
    base_url=os.environ.get("OPENAI_BASE_URL", "http://127.0.0.1:8080/v1"),
    default_headers={"x-deadweight-app": "openai-story-flow"}), use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(True)
MODEL = os.environ.get("STORY_MODEL", "gpt-4o-mini")

"""
This example demonstrates a deterministic flow, where each step is performed by an agent.
1. The first agent generates a story outline
2. We feed the outline into the second agent
3. The second agent checks if the outline is good quality and if it is a scifi story
4. If the outline is not good quality or not a scifi story, we stop here
5. If the outline is good quality and a scifi story, we feed the outline into the third agent
6. The third agent writes the story
"""

story_outline_agent = Agent(
    name="story_outline_agent",
    instructions="Generate a very short story outline based on the user's input.",
    model=MODEL,  # DEADWEIGHT
)


class OutlineCheckerOutput(BaseModel):
    good_quality: bool
    is_scifi: bool


outline_checker_agent = Agent(
    name="outline_checker_agent",
    instructions="Read the given story outline, and judge the quality. Also, determine if it is a scifi story.",
    output_type=OutlineCheckerOutput,
    model=MODEL,  # DEADWEIGHT
)

story_agent = Agent(
    name="story_agent",
    instructions="Write a short story based on the given outline.",
    output_type=str,
    model=MODEL,  # DEADWEIGHT
)


async def main(input_prompt):  # DEADWEIGHT : demande en argument
    # Ensure the entire workflow is a single trace
    with trace("Deterministic story flow"):
        # 1. Generate an outline
        outline_result = await Runner.run(
            story_outline_agent,
            input_prompt,
        )
        print("Outline generated")

        # 2. Check the outline
        outline_checker_result = await Runner.run(
            outline_checker_agent,
            outline_result.final_output,
        )

        # 3. Add a gate to stop if the outline is not good quality or not a scifi story
        assert isinstance(outline_checker_result.final_output, OutlineCheckerOutput)
        if not outline_checker_result.final_output.good_quality:
            print("Outline is not good quality, so we stop here.")
            return  # DEADWEIGHT : au lieu de exit(0)

        if not outline_checker_result.final_output.is_scifi:
            print("Outline is not a scifi story, so we stop here.")
            return  # DEADWEIGHT : au lieu de exit(0)

        print("Outline is good quality and a scifi story, so we continue to write the story.")

        # 4. Write the story
        story_result = await Runner.run(
            story_agent,
            outline_result.final_output,
        )
        print(f"Story: {story_result.final_output}")


if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:]) or "Write a short sci-fi story."))
