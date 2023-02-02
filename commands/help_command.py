import discord
from discord import app_commands
from discord.ext import commands

from settings import embed_color


class HelpCommand(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(
        name="help",
        description="Information about bot commands"
    )
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Info",
            description="This bot generates the answer to your questions using the OpenAi library. "
            "All commands use a set of **GPT-3** models that can understand and generate natural language. "
            "At the moment, the most effective GPT-3 model is `text-davinci-003`, which you can use "
            "with the `/ask_davinci` command. "
            "You can find out about this and other models on the "
            "[official website](https://platform.openai.com/docs/models)",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(HelpCommand(client))

