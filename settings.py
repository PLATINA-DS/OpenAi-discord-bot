import os
from dotenv import load_dotenv


load_dotenv()

# Keys, Tokens
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embed_color = 0x36393F
