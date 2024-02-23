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
		intent.guilds = True
		intent.members = False
		self.token = os.getenv("DISCORD_BOT_TOKEN")
		self.pwhost =  os.getenv("PALWORLD_RCON_HOST")
		self.pwpasswrd = os.getenv("PALWORLD_RCON_PASSWORD")
		self.pwport = int(os.getenv("PALWORLD_RCON_PORT"))
		self.srvpath = os.getenv("SERVER_PATH")
		self.prefix = os.getenv("DISCORD_COMMAND_PREFIX")
		super().__init__(self.prefix, help_command=None, intents=intent, tree_cls=CommandTree)

	async def setup_hook(self):
		for extension in EXTENSIONS:
			await self.load_extension(extension)