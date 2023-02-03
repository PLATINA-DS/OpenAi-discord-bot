import discord
from time import time
import openai
from typing import Optional

from settings import embed_color


async def generator(model: str, deco_model_name: str, prompt: str) -> Optional[discord.Embed]:
    generation_start = time()
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=1024,
        temperature=0.4
    )
    generation_finish = time()
    generation_time = int(generation_finish - generation_start)
    answer = response.get('choices')[0].get('text')
    answer = f"{answer[:1021]}..." if len(answer) > 1024 else answer
    embed = discord.Embed(
        title="Result",
        color=embed_color
    )

    embed.set_author(name=f"Model - {deco_model_name}")
    embed.add_field(name="Question", value=prompt, inline=False)
    embed.add_field(name="Answer", value=answer, inline=False)
    embed.set_footer(text=f"Generation time - {generation_time}s")

    return embed
