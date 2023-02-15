import discord
from discord import app_commands
from discord.ext import commands
from io import BytesIO

from settings import embed_color


class SendExampleCommand(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(
        name="send_example",
        description="Show an example of using the bot"
    )
    async def send_example(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Example of using the bot", color=embed_color)
        embed.set_image(url="https://s9.gifyu.com/images/example1456c05bf2b18efb.gif")

        await interaction.response.send_message(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(SendExampleCommand(client))