import discord
from time import time
import aiohttp

from settings import embed_color, OPENAI_API_KEY


async def generate(model: str, prompt: str) -> str:
    async with aiohttp.ClientSession() as session:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_API_KEY}'
        }
        data = {
            'prompt': prompt,
            'temperature': 0.7,
            'max_tokens': 1024
        }

        async with session.post(f'https://api.openai.com/v1/engines/{model}/completions',
                                headers=headers, json=data) as resp:
            response_data = await resp.json()
            response_text = response_data.get("choices")[0].get("text")

    answer = f"{response_text[:1021]}..." if len(response_text) > 1024 else response_text

    return answer


async def timer(model: str, prompt: str) -> int and str:
    start = time()
    answer = await generate(model, prompt)
    end = time()
    result = int(end - start)

    return result, answer


async def generated_embed(model: str, deco_model_name: str, prompt: str) -> discord.Embed:
    generation_time, answer = await timer(model, prompt)
    embed = discord.Embed(
        title="Result",
        color=embed_color
    )
    embed.set_author(name=f"Model - {deco_model_name}")
    embed.add_field(name="Question", value=prompt, inline=False)
    embed.add_field(name="Answer", value=answer, inline=False)
    embed.set_footer(text=f"Generation time - {generation_time}s")

    return embed
