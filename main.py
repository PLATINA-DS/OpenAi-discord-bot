import discord
import openai
from discord import app_commands
from discord.ext import commands
import asyncio

from settings import BOT_TOKEN, OPENAI_API_KEY, embed_color


openai.api_key = OPENAI_API_KEY


class Client(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix="/",
            help_command=None,
            intents=discord.Intents.all()
        )

    async def setup_hook(self):
        await self.load_extension("commands.ask_command")
        await self.load_extension("commands.help_command")
        await self.load_extension("commands.send_example")

        await self.tree.sync(guild=None)

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="https://github.com/PLATINA-DS/OpenAi-discord-bot"),
                                   status=discord.Status.idle)

        print("connected")


client = Client()


@client.tree.error
async def on_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.CommandOnCooldown):
        embed = discord.Embed(
            description=f"Try again after **{round(error.retry_after)}s**",
            color=embed_color
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        raise error


async def main():
    async with client:
        await client.start(BOT_TOKEN)

asyncio.run(main())
