import discord, os, platform, pathlib, asyncio
from discord.ext import commands
from discord import app_commands

from ..lib.checkUptime import check_port

from ..views.sm import ShutdownConfirmationView

PALWORLD_RCON_HOST = "127.0.0.1"
PALWORLD_PORT = 8211
SERVER_PATH = str(pathlib.Path(__file__).parents[3])

class ServerManagementCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def cog_load(self):
		print(f"{self.__class__.__name__}\n----------------------------------------")

	servercommand = app_commands.Group(name="server", description="group of commands to manage Palworld Server")

	@servercommand.command(name="start", description="Startet den Palworld Server.")
	async def sstart(self, interaction: discord.Interaction):
		terminal = os.system
		if platform.system() == "Windows":
			path = SERVER_PATH + "/start.bat"
		elif platform.system() == "Linux":
			path = "systemctl start palworld"
		embed = discord.Embed(title="Bitte warten", description="Server wird gestartet.", color=discord.Colour.blue())
		await interaction.response.send_message(embed=embed)
		if check_port(PALWORLD_RCON_HOST, PALWORLD_PORT):
			embed = discord.Embed(title="Server läuft bereits.", color=discord.Colour.red())
			await interaction.edit_original_response(embed=embed)
			return
		terminal(path)
		await asyncio.sleep(float(10))
		if check_port(PALWORLD_RCON_HOST, PALWORLD_PORT):
			embed = discord.Embed(title="Starten erfolgreich!", colour=discord.Colour.green())
		else:
			embed = discord.Embed(title="Starten fehlgeschlagen!", description="Server konnte nicht gestartet werden.", colour=discord.Colour.red())
		await interaction.edit_original_response(embed=embed)

	@servercommand.command(name="shutdown", description="Fährt den Server herunter.")
	async def sshutdown(self, interaction: discord.Interaction, seconds: int=None, message: str=None):
		embed = discord.Embed(title="Server herunterfahren", description=f"Bist du dir sicher, dass du den Server {f'in {seconds} Sekunden ' if seconds != None else ''}{f'mit der Nachricht {message} ' if message != None else ''}herunterfahren möchtest?", color=discord.Colour.yellow())
		view = ShutdownConfirmationView(seconds, message)
		await interaction.response.send_message(embed=embed, view=view)
		view.message = await interaction.original_response()

async def setup(bot):
	await bot.add_cog(ServerManagementCog(bot))