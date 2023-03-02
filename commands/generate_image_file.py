import discord
from discord import app_commands
from discord.ext import commands

from response_generator.image_file_generator import generate_answer_embed
from buttons.regenerate_image_file import RegenerateImageButton
from cooldown_factory.cooldown import ask_command_cooldown


class GenerateImageFileCommand(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(
        name="image_file",
        description="Image file generation. Slower than /image_link"
    )
    @app_commands.checks.dynamic_cooldown(ask_command_cooldown)
    async def generate_image_file_command(self, interaction: discord.Interaction, prompt: str):
        regenerate_response_button = RegenerateImageButton(prompt, interaction.user)

        await interaction.response.defer()
        embed, file = await generate_answer_embed(prompt)
        await interaction.followup.send(embed=embed, file=file, view=regenerate_response_button)


async def setup(client: commands.Bot):
    await client.add_cog(GenerateImageFileCommand(client))
