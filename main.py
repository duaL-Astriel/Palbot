import pathlib
from src.lib.bot import PalBot
from src.lib.config import *
from dotenv import load_dotenv

load_dotenv(".env")

# print("Server path is: " + SERVER_PATH)
print("Current path is: " + str(pathlib.Path(__file__).parents[1]))

bot = PalBot()

bot.run(bot.token)