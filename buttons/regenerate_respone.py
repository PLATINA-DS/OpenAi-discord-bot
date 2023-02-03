import discord
from discord import ui
from discord.ext import commands

from response_generator.generator import generator
from settings import embed_color


class RegenerateButton(ui.View):
    def __init__(self, model: str, deco_model_name: str, prompt: str, author: discord.Member) -> None:
        super().__init__(timeout=180)

        self.model = model
        self.deco_model_name = deco_model_name
        self.prompt = prompt
        self.author = author
        self._cooldown = commands.CooldownMapping.from_cooldown(1, 10, commands.BucketType.member)

    @ui.button(label="Regenerate response", style=discord.ButtonStyle.green)
    async def regenerate(self, interaction: discord.Interaction, _):
        if interaction.user != self.author:
            embed = discord.Embed(
                description="You can't use it because you're not the person who asked the question",
                color=embed_color
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        bucket = self._cooldown.get_bucket(interaction.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            embed = discord.Embed(
                description=f"You will be able to use the button again after **{round(retry_after, 1)}** seconds",
                color=embed_color
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True
                                                           )
        await interaction.response.defer()

        embed = await generator(self.model, self.deco_model_name, self.prompt)

        await interaction.edit_original_response(embed=embed, view=self)
