import discord
from discord import app_commands
from discord.ext import commands

from settings import embed_color


class HelpCommand(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(
        name="help",
        description="Information about bot commands"
    )
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Info",
            description="This bot generates the answer to your questions using the OpenAi library. "
            "All commands use a set of **GPT-3** models that can understand and generate natural language. "
            "At the moment, the most effective GPT-3 model is `text-davinci-003`, which you can use "
            "with the `/ask` command. "
            "You can find out about this and other models on the "
            "[official website](https://platform.openai.com/docs/models/gpt-3)\n\n"
            "This is not an official OpenAI bot. "
            "This bot simply provides the ability to use "
            "the capabilities of different models developed by this company in discord chats\n\n"
            "This bot is fully open source available on [github](https://github.com/PLATINA-DS/OpenAi-discord-bot)",
            color=embed_color
        )
        embed.add_field(name="Model - text-davinci-003",
                        value="Most capable GPT-3 model. "
                              "Can do any task the other models can do, "
                              "often with higher quality, longer output "
                              "and better instruction-following. "
                              "Also supports inserting completions within text.")
        embed.add_field(name="Other models",
                        value="You can find out about this and other models on the "
                        "[official website](https://platform.openai.com/docs/models/gpt-3)")
        embed.add_field(name="How to use?",
                        value="Using this bot is very easy. "
                        "**Write** the `/ask` command in the chat, "
                        "**select** the model you want to use, "
                        "**write** your question or task, and wait for an answer.\n"
                        "The **regenerate response** button will change the bot's response "
                        "if you don't like it.\n"
                        "Remember that this is artificial intelligence, "
                        "and the better you describe what you need, the better the answer will be.",
                        inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(HelpCommand(client))

