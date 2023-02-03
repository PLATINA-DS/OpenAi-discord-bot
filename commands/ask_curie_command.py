import discord
from discord import app_commands
from discord.ext import commands

from response_generator.generator import generator
from buttons.regenerate_respone import RegenerateButton
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
        model, deco_model_name = "text-curie-001", "curie"
        regenerate_response_button = RegenerateButton(model, deco_model_name, prompt, interaction.user)

        await interaction.response.defer()
        embed = await generator(model, deco_model_name, prompt)
        await interaction.followup.send(embed=embed, view=regenerate_response_button)


async def setup(client: commands.Bot):
    await client.add_cog(AskCurieCommand(client))
