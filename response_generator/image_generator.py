import discord
from time import time
import aiohttp

from settings import embed_color, OPENAI_API_KEY


async def generate(prompt: str) -> str:
    async with aiohttp.ClientSession() as session:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_API_KEY}'
        }
        data = {
            'prompt': prompt,
            'n': 1,
            'size': "1024x1024"
        }

        async with session.post('https://api.openai.com/v1/images/generations',
                                headers=headers, json=data) as resp:
            response_data = await resp.json()
            image_url = response_data.get("data")[0].get("url")

    return image_url


async def timer(prompt: str) -> int and str:
    start = time()
    image_url = await generate(prompt)
    end = time()
    result = int(end - start)

    return result, image_url


async def generated_embed(prompt: str) -> discord.Embed:
    generation_time, image_url = await timer(prompt)
    embed = discord.Embed(
        title="Result",
        color=embed_color
    )
    embed.add_field(name="Prompt", value=prompt, inline=False)
    embed.set_image(url=image_url)
    embed.set_footer(text=f"Generation time - {generation_time}s")

    return embed
