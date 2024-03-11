import discord, asyncio, traceback, sys
from discord.ui import View, Button, button
from ..lib.client import Console
from ..lib.bot import PalBot
from ..lib.check_uptime import is_application_running, is_service_running

PALWORLD_APPLICATION_NAME = "PalServer-Win64-Test-Cmd.exe"
PALWORLD_SERVICE_NAME = "palworld"

class ShutdownConfirmationView(View):
	def __init__(self, seconds: int=None, message=None):
		self.seconds: str = seconds
		self.msg: str = message
		self.bot = PalBot()
		super().__init__(timeout=30)
	
	@button(label="Bestätigen", style=discord.ButtonStyle.green)
	async def sconfirmation(self, interaction: discord.Interaction, button: Button):
		await interaction.response.edit_message(embed=discord.Embed(title="Bitte warten", description="Server wird heruntergefahren."), view=None)
		
		if not self.seconds:
			self.seconds = "0"
		try:
			rcon_client = Console
			# remove spaces
			if self.msg == "":
				formatted_message = self.msg.replace(" ", "_")
				response = rcon_client.shutdown(self.seconds, formatted_message)
				print(response)
					
			else:
				response = rcon_client.shutdown(self.seconds)
				print(response)
		except Exception as e:
			print(f"Unable to shutdown game server: ")
			traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
			await interaction.edit_original_response(embed=discord.Embed(title="Fehlgeschlagen!", description="Server konnte nicht heruntergefahren werden."), view=None)
			return
		
		await asyncio.sleep(float(5 + int(self.seconds)))

		if not is_application_running(PALWORLD_APPLICATION_NAME) and not is_service_running(PALWORLD_SERVICE_NAME):
			print("Successfully shut down server.")
			await interaction.edit_original_response(embed=discord.Embed(title="Erfolgreich!", description="Server wurde erfolgreich heruntergefahren."), view=None)
	
	@button(label="Abbrechen", style=discord.ButtonStyle.danger)
	async def sdenied(self, interaction: discord.Interaction, button: Button):
		await interaction.response.edit_message(embed=discord.Embed(title="Abgebrochen", description="Shutdown vom Benutzer abgebrochen."), view=None)