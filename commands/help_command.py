import discord
from discord import app_commands
from discord.ext import commands

from settings import embed_color
from texts import *


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
            description=info,
            color=embed_color
        )
        embed.add_field(name="Model - text-davinci-003",
                        value=davinci_description)
        embed.add_field(name="Other models",
                        value=project_share)
        embed.add_field(name="How to use?",
                        value=tutorial,
                        inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(HelpCommand(client))
