import discord
from discord import app_commands
from discord.ext import commands

from response_generator.image_generator import generated_embed
from buttons.regenerate_image import RegenerateImageButton
from cooldown_factory.cooldown import ask_command_cooldown


class GenerateImageCommand(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(
        name="image",
        description="Image generation"
    )
    @app_commands.checks.dynamic_cooldown(ask_command_cooldown)
    async def generate_image(self, interaction: discord.Interaction, prompt: str):
        regenerate_response_button = RegenerateImageButton(prompt, interaction.user)

        await interaction.response.defer()
        embed = await generated_embed(prompt)
        await interaction.followup.send(embed=embed, view=regenerate_response_button)


async def setup(client: commands.Bot):
    await client.add_cog(GenerateImageCommand(client))
