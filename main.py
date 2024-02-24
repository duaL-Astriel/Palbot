import pathlib
from src.lib.bot import PalBot
from src.lib.config import *
from dotenv import load_dotenv

load_dotenv(".env")

bot = PalBot()

bot.run(bot.token)