import discord
from discord import ui
from discord.ext import commands

from response_generator.image_link_generator import generate_answer_embed
from settings import embed_color


class RegenerateImageLinkButton(ui.View):
    def __init__(self, prompt: str, author: discord.Member) -> None:
        super().__init__(timeout=180)

        self.prompt = prompt
        self.author = author
        self._cooldown = commands.CooldownMapping.from_cooldown(1, 10, commands.BucketType.member)
        self._button_usages = 0

    @ui.button(label="Regenerate image", style=discord.ButtonStyle.green)
    async def regenerate(self, interaction: discord.Interaction, *args):
        bucket = self._cooldown.get_bucket(interaction.message)
        retry_after = bucket.update_rate_limit()
        regenerate_embed = discord.Embed(description="Image link regeneration...",
                                         color=embed_color)
        not_available_embed = discord.Embed(description="Image link regeneration is available only 3 times",
                                            color=embed_color)

        if interaction.user != self.author:
            embed = discord.Embed(
                description="You can't use it because you're not the person who asked the image",
                color=embed_color
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if retry_after:
            embed = discord.Embed(
                description=f"You will be able to use the button again after **{round(retry_after, 1)}** seconds",
                color=embed_color
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if self._button_usages >= 3:
            await interaction.message.edit(view=None)
            await interaction.response.send_message(embed=not_available_embed, ephemeral=True)
            return
        await interaction.message.edit(embed=regenerate_embed, view=None, attachments=[])
        await interaction.response.defer()
        embed = await generate_answer_embed(self.prompt)
        await interaction.edit_original_response(embed=embed, view=self)

        self._button_usages += 1
