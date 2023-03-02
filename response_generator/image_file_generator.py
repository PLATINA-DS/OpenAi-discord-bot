import discord
from time import time
import aiohttp
import tempfile

from settings import embed_color, OPENAI_API_KEY


class OpenAIResponse:
    def __init__(self, execution_time: float, image_url: str):
        self.execution_time = execution_time
        self.image_url = image_url


async def __request_to_openai(prompt: str) -> OpenAIResponse:
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

        return OpenAIResponse(request_execution_time, image_url)


async def __download_image(prompt: str) -> str:
    request_result = await __request_to_openai(prompt)
    image_url = request_result.image_url
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)

            return f.name


async def __convert_image_to_discord_file(prompt: str) -> discord.File:
    file_path = await __download_image(prompt)
    file = discord.File(file_path)

    return file


async def generate_answer_embed(prompt: str) -> tuple[discord.Embed, discord.File]:
    image_file = await __convert_image_to_discord_file(prompt)
    openai_response = await __request_to_openai(prompt)
    request_execution_time = openai_response.execution_time
    embed = discord.Embed(
        color=embed_color
    )
    embed.add_field(name="Prompt", value=prompt, inline=False)
    embed.set_image(url=f"attachment://{image_file.filename}")
    embed.set_footer(text=f"Generation time - {request_execution_time}s")

    return embed, image_file
