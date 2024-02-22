import discord, pathlib, os
from discord.ext import commands
from discord.app_commands import CommandTree
from dotenv import load_dotenv
path = str(pathlib.Path(__file__).parents[3])
load_dotenv(path+"/.env")

from ..cogs import EXTENSIONS

class PalBot(commands.Bot):
	def __init__(self) -> None:
		intent = discord.Intents.none()
		intent.members = False
		self.token = os.environ["DISCORD_BOT_TOKEN"]
		self.pwhost =  os.environ["PALWORLD_RCON_HOST"]
		self.pwpasswrd = os.environ["PALWORLD_RCON_PASSWORD"]
		self.pwport = os.environ["PALWORLD_RCON_PORT"]
		super().__init__("!pb", help_command=None, intents=intent, tree_cls=CommandTree)

	async def setup_hook(self):
		for extension in EXTENSIONS:
			await self.load_extension(extension)

