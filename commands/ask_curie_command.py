import discord
import openai
from discord import app_commands
from discord.ext import commands
from time import time

from settings import embed_color
from cooldown_factory.cooldown import ask_command_cooldown


class AskCurieCommand(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(
        name="ask_curie",
        description="Ask curie model a question"
    )
    @app_commands.checks.dynamic_cooldown(ask_command_cooldown)
    async def ask_curie(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()

        generation_start = time()
        response = openai.Completion.create(
            model="text-curie-001",
            prompt=prompt,
            max_tokens=1024,
            temperature=0.4
        )
        generation_finish = time()
        generation_time = int(generation_finish - generation_start)
        answer = response.get("choices")[0].get("text")

        embed = discord.Embed(
            title="Result",
            color=embed_color
        )
        embed.set_author(name="Model - curie")
        embed.add_field(name="Question", value=prompt, inline=False)
        embed.add_field(name="Answer", value=answer, inline=False)
        embed.set_footer(text=f"Generation time - {generation_time}s")

        await interaction.followup.send(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(AskCurieCommand(client))
