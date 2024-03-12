import discord, asyncio, traceback, sys
from discord.ui import View, Button, button
from ..lib.client import Rcon_Client
from ..lib.bot import PalBot
from ..lib.check_uptime import is_application_running, is_service_running

PALWORLD_APPLICATION_NAME = "PalServer-Win64-Test-Cmd.exe"
PALWORLD_SERVICE_NAME = "palworld"

class ShutdownConfirmationView(View):
	def __init__(self, seconds, message):
		self.seconds = seconds
		self.msg = message
		self.bot = PalBot()
		super().__init__(timeout=30)
	
	@button(label="Bestätigen", style=discord.ButtonStyle.green)
	async def sconfirmation(self, interaction: discord.Interaction, button: Button):
		await interaction.response.edit_message(embed=discord.Embed(title="Bitte warten", description="Server wird heruntergefahren."), color=discord.Colour.yellow(), view=None)
		
		try:
			rcon_client = Rcon_Client
			response = await rcon_client.rcon_command(self=rcon_client,command=f"Shutdown {self.seconds} {self.msg}")
			print(response)

			waiting_counter = 60 + self.seconds
			while waiting_counter != 0:
				if not is_application_running(PALWORLD_APPLICATION_NAME) and not is_service_running(PALWORLD_SERVICE_NAME):
					print("Successfully shut down server.")
					await interaction.edit_original_response(embed=discord.Embed(title="Erfolgreich!", description="Server wurde erfolgreich heruntergefahren.", color=discord.Colour.green()), view=None)
					return
				await asyncio.sleep(1)
				waiting_counter -= 1
			await interaction.edit_original_response(embed=discord.Embed(title="Fehlgeschlagen!", description="Timeout beim Herunterfahren.", color=discord.Colour.red()), view=None)	
				
		except Exception as e:
			print(f"Unable to shutdown game server: ")
			traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
			await interaction.edit_original_response(embed=discord.Embed(title="Fehlgeschlagen!", description="Server konnte nicht heruntergefahren werden.", color=discord.Colour.red()), view=None)
			return
	
	@button(label="Abbrechen", style=discord.ButtonStyle.danger)
	async def sdenied(self, interaction: discord.Interaction, button: Button):
		await interaction.response.edit_message(embed=discord.Embed(title="Abgebrochen", description="Shutdown vom Benutzer abgebrochen.", color=discord.Colour.blurple()), view=None)