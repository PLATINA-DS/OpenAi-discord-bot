import discord
from discord import app_commands
from discord.ext import commands

from response_generator.image_link_generator import generate_answer_embed
from buttons.regenerate_image_link import RegenerateImageLinkButton
from cooldown_factory.cooldown import ask_command_cooldown


class GenerateImageLinkCommand(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(
        name="image_link",
        description="Image link generation. Faster than /image_file"
    )
    @app_commands.checks.dynamic_cooldown(ask_command_cooldown)
    async def generate_image_link(self, interaction: discord.Interaction, prompt: str):
        regenerate_response_button = RegenerateImageLinkButton(prompt, interaction.user)

        await interaction.response.defer()
        embed = await generate_answer_embed(prompt)
        await interaction.followup.send(embed=embed, view=regenerate_response_button)


async def setup(client: commands.Bot):
    await client.add_cog(GenerateImageLinkCommand(client))
