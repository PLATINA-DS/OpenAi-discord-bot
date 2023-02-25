import discord
from discord import app_commands
from typing import Optional


def ask_command_cooldown(interaction: discord.Interaction) -> app_commands.Cooldown:
    return app_commands.Cooldown(1, 20.0)
