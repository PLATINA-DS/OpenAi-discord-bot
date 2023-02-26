from discord import app_commands


def ask_command_cooldown(*args) -> app_commands.Cooldown:
    return app_commands.Cooldown(1, 20.0)
