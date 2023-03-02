import discord
from time import time
import aiohttp

from settings import embed_color, OPENAI_API_KEY


async def __request_to_openai(prompt: str) -> tuple[int, str]:
    start = time()

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
            image_url = response_data["data"][0]["url"]

        end = time()
        request_execution_time = round(end - start)

        return request_execution_time, image_url


async def generate_answer_embed(prompt: str) -> discord.Embed:
    request_execution_time, image_url = await __request_to_openai(prompt)
    embed = discord.Embed(
        title="Result",
        color=embed_color
    )
    embed.add_field(name="Prompt", value=prompt, inline=False)
    embed.set_image(url=image_url)
    embed.set_footer(text=f"Generation time - {request_execution_time}s")

    return embed






