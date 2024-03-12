import discord
from discord.ext import commands, tasks
from discord.app_commands import CommandTree
from .config import *

from .backup import zip_and_backup_palworld
from ..cogs import EXTENSIONS

class PalBot(commands.Bot):
	def __init__(self) -> None:
		intents = discord.Intents.none()
		intents.guilds = True
		intents.members = False
		intents.message_content = True
		intents.guild_messages = True
		self.token = DISCORD_BOT_TOKEN
		self.pwhost =  PALWORLD_RCON_HOST
		self.pwpasswrd = PALWORLD_RCON_PASSWORD
		self.pwport = PALWORLD_RCON_PORT
		self.srvpath = SERVER_PATH
		self.prefix = DISCORD_COMMAND_PREFIX
		super().__init__(command_prefix=self.prefix, help_command=None, intents=intents, tree_cls=CommandTree)

	async def setup_hook(self):
		for extension in EXTENSIONS:
			await self.load_extension(extension)
		
	async def on_message(self, message: discord.Message) -> None:
		await self.process_commands(message)

	
	
	# @tasks.loop(hours=1)
	# async def backuploop(self):
	# 	await zip_and_backup_palworld()
		