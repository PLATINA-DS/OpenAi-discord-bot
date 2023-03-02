import discord
from discord import app_commands
from discord.ext import commands

from response_generator.text_answer_generator import generate_answer_embed
from buttons.regenerate_respone import RegenerateButton
from cooldown_factory.cooldown import ask_command_cooldown


class AskCommand(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(
        name="ask",
        description="Ask model a question"
    )
    @app_commands.choices(model=[
        app_commands.Choice(name="Davinci", value="text-davinci-003"),
        app_commands.Choice(name="Curie", value="text-curie-001"),
        app_commands.Choice(name="Babbage", value="text-babbage-001"),
        app_commands.Choice(name="Ada", value="text-ada-001")
    ])
    @app_commands.checks.dynamic_cooldown(ask_command_cooldown)
    async def ask_davinci(self, interaction: discord.Interaction, model: app_commands.Choice[str], prompt: str):
        model, deco_model_name = model.value, model.name
        regenerate_response_button = RegenerateButton(model, deco_model_name, prompt, interaction.user)

        await interaction.response.defer()
        embed = await generate_answer_embed(model, deco_model_name, prompt)
        await interaction.followup.send(embed=embed, view=regenerate_response_button)


async def setup(client: commands.Bot):
    await client.add_cog(AskCommand(client))
