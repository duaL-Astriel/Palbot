import os
import discord, platform, pathlib, asyncio
from discord.ext import commands
from discord import app_commands

from ..lib.check_uptime import is_application_running, is_service_running

from ..views.sm import ShutdownConfirmationView

PALWORLD_APPLICATION_NAME = "PalServer-Win64-Test-Cmd.exe"
PALWORLD_SERVICE_NAME = "palworld"
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
		await interaction.response.defer(thinking=True)
		
		if is_application_running(PALWORLD_APPLICATION_NAME) or is_service_running(PALWORLD_SERVICE_NAME):
			print("Server start command received, but server is already running.")
			await interaction.followup.send(embed=discord.Embed(title="Server läuft bereits.", color=discord.Colour.red()))
			return
		
		print("Starting Palworld server...")
		terminal = os.system

		if platform.system() == "Windows":
			print("System is Windows")
			start_command = "C:/Users/Plex/Desktop/Palworld/start.bat"

		elif platform.system() == "Linux":
			print("System is Linux")
			start_command = "systemctl start palworld"
		
		await interaction.followup.send(embed=discord.Embed(title="Bitte warten", description="Server wird gestartet.", color=discord.Colour.blue()))
		terminal(start_command)

		waiting_counter = 30
		while waiting_counter != 0:
			if is_application_running(PALWORLD_APPLICATION_NAME) or is_service_running(PALWORLD_SERVICE_NAME):
				await interaction.edit_original_response(embed=discord.Embed(title="Starten erfolgreich!", colour=discord.Colour.green()))
				return
			await asyncio.sleep(1)
			waiting_counter -= 1
			
		await interaction.edit_original_response(embed=discord.Embed(title="Starten fehlgeschlagen!", description=f"Server konnte nicht gestartet werden.", colour=discord.Colour.red()))

	@servercommand.command(name="shutdown", description="Fährt den Server herunter.")
	async def sshutdown(self, interaction: discord.Interaction, seconds: int = 10, message: str = " "):
		if not is_application_running(PALWORLD_APPLICATION_NAME) and not is_service_running(PALWORLD_SERVICE_NAME):
			await interaction.response.send_message(embed=discord.Embed(title="Server läuft nicht."))
			return
		embed = discord.Embed(title="Server herunterfahren", description=f"Bist du dir sicher, dass du den Server {f'in {seconds} Sekunden ' if seconds != None else ''}{f'mit der Nachricht {message} ' if message != None else ''}herunterfahren möchtest?", color=discord.Colour.blurple())
		view = ShutdownConfirmationView(seconds, message)
		await interaction.response.send_message(embed=embed, view=view)
		view.message = await interaction.original_response()

async def setup(bot):
	await bot.add_cog(ServerManagementCog(bot))