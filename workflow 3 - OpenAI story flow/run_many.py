"""Lance story_flow.py une fois par ligne de prompts.txt (même processus, à la suite)."""
import asyncio
from pathlib import Path

from story_flow import main

PROMPTS = [p for p in (Path(__file__).parent / "prompts.txt").read_text().splitlines() if p.strip()]


async def run_all():
    for i, prompt in enumerate(PROMPTS, 1):
        print(f"\n=== {i}/{len(PROMPTS)} : {prompt}")
        await main(prompt)

asyncio.run(run_all())
