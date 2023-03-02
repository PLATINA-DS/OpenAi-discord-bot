import discord
from discord import app_commands
from discord.ext import commands
import asyncio

from settings import BOT_TOKEN, embed_color


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
        await self.load_extension("commands.generate_image_file")
        await self.load_extension("commands.generate_image_link")

        await self.tree.sync(guild=None)

    async def on_ready(self):
        guilds_count = len(self.guilds)
        users_count = len(set(self.get_all_members()))

        await self.change_presence(activity=discord.Game(
            name=f"Responsible for {guilds_count} guilds with "
                 f"{users_count} users"),
            status=discord.Status.idle)
        print("connected")

    async def on_guild_join(self, *args):
        guilds_count = len(self.guilds)
        users_count = len(set(self.get_all_members()))

        await self.change_presence(activity=discord.Game(
            name=f"Responsible for {guilds_count} guilds with "
                 f"{users_count} users"),
            status=discord.Status.idle)

    async def on_guild_remove(self, *args):
        guilds_count = len(self.guilds)
        users_count = len(set(self.get_all_members()))

        await self.change_presence(activity=discord.Game(
            name=f"Responsible for {guilds_count} guilds with "
                 f"{users_count} users"),
            status=discord.Status.idle)


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
