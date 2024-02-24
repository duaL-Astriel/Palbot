import discord, platform, pathlib, asyncio, subprocess
from discord.ext import commands
from discord import app_commands

from ..lib.check_uptime import udp_ping, is_application_running
from ..lib.service_running import is_service_running

from ..views.sm import ShutdownConfirmationView

PALWORLD_APPLICATION_NAME = "PalServer-Win64-Test-Cmd.exe"
PALWORLD_HOST = "127.0.0.1"
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
		await interaction.response.send_message(embed=discord.Embed(title="Bitte warten", description="Server wird gestartet.", color=discord.Colour.blue()))
		
		if platform.system() == "Windows":
			start_command = SERVER_PATH + "/start.bat"
			if is_application_running(PALWORLD_APPLICATION_NAME):
				await interaction.edit_original_response(embed=discord.Embed(title="Server läuft bereits.", color=discord.Colour.red()))
				return

		elif platform.system() == "Linux":
			print("System is Linux")
			start_command = "systemctl start palworld"
			if is_service_running("palworld"):
				await interaction.edit_original_response(embed=discord.Embed(title="Server läuft bereits.", color=discord.Colour.red()))
				return
		
		result = subprocess.run(start_command, shell=True, capture_output=True, text=True)
		if not result.stdout:
			print(f"Command result: {result.stdout}")
		await asyncio.sleep(float(10))

		if udp_ping(PALWORLD_HOST, PALWORLD_PORT):
			embed = discord.Embed(title="Starten erfolgreich!", colour=discord.Colour.green())

		else:
			embed = discord.Embed(title="Starten fehlgeschlagen!", description=f"Server konnte nicht gestartet werden.\n{result.stdout}", colour=discord.Colour.red())
			
		await interaction.edit_original_response(embed=embed)

	@servercommand.command(name="shutdown", description="Fährt den Server herunter.")
	async def sshutdown(self, interaction: discord.Interaction, seconds: int=None, message: str=None):
		embed = discord.Embed(title="Server herunterfahren", description=f"Bist du dir sicher, dass du den Server {f'in {seconds} Sekunden ' if seconds != None else ''}{f'mit der Nachricht {message} ' if message != None else ''}herunterfahren möchtest?", color=discord.Colour.yellow())
		view = ShutdownConfirmationView(seconds, message)
		await interaction.response.send_message(embed=embed, view=view)
		view.message = await interaction.original_response()

async def setup(bot):
	await bot.add_cog(ServerManagementCog(bot))