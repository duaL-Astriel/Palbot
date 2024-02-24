import discord, asyncio
from discord.ui import View, Button, button
from ..lib.client import Client
from ..lib.bot import PalBot
from ..lib.check_uptime import is_application_running

PALWORLD_APPLICATION_NAME = "PalServer-Win64-Test-Cmd.exe"

class ShutdownConfirmationView(View):
	def __init__(self, seconds: int=None, message=None):
		self.seconds: str = seconds
		self.msg: str = message
		self.bot = PalBot()
		super().__init__(timeout=30)
	
	@button(label="Bestätigen", style=discord.ButtonStyle.green)
	async def sconfirmation(self, interaction: discord.Interaction, button: Button):
		await interaction.response.edit_message(embed=discord.Embed(title="Am Herunterfahren", description="Bitte warten. Server wird heruntergefahren."), view=None)
		if not self.seconds:
			self.seconds = 0
		try:
			rcon_client = Client()
			# remove spaces
			formatted_message = ""
			if self.msg:
				formatted_message = self.msg.replace(" ", "_")
			response = rcon_client.shutdown(self.seconds, formatted_message)
		except Exception as e:
			print(f"Unable to shutdown game server: {e}")
			await interaction.edit_original_response(embed=discord.Embed(title="Fehlgeschlagen!", description="Server konnte nicht heruntergefahren werden.\n" + response), view=None)
			return
			
		await asyncio.sleep(float(3 + self.seconds))

		if not is_application_running(PALWORLD_APPLICATION_NAME):
			await interaction.edit_original_response(embed=discord.Embed(title="Erfolgreich!", description="Server wurde erfolgreich heruntergefahren."), view=None)
	
	@button(label="Abbrechen", style=discord.ButtonStyle.danger)
	async def sdenied(self, interaction: discord.Interaction, button: Button):
		await interaction.edit_original_response(embed=discord.Embed(title="Abgebrochen", description="Shutdown vom Benutzer abgebrochen."), view=None)