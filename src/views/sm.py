import discord, asyncio
from discord.ui import View, Button, button
from rcon.source import rcon
from ..lib.bot import PalBot

class ShutdownConfirmationView(View):
	def __init__(self, seconds: int=None, message=None):
		self.seconds = seconds
		self.msg = message
		self.bot = PalBot()
		super().__init__(timeout=30)
	
	@button(label="Bestätigen", style=discord.ButtonStyle.danger)
	async def sconfirmation(self, interaction: discord.Interaction, button: Button):
		
		if self.seconds != None:
			embed = discord.Embed(title="Erfolgreich", description=f"Server wird in {self.seconds} sekunden heruntergefahren\n{f'Nachricht: {self.msg}' if self.msg is not None else ''}", color=discord.Colour.green())
			await interaction.response.edit_message(embed=embed, view=None)
			await asyncio.sleep(float(self.seconds))
			await rcon("shutdown", host=self.bot.pwhost, port=self.bot.pwport, passwd=self.bot.pwpasswrd)
		else: 
			await rcon("shutdown", host=self.bot.pwhost, port=self.bot.pwport, passwd=self.bot.pwpasswrd)
			embed = discord.Embed(title="Erfolgreich", description="Server wurde erfolgreich heruntergefahren")
			await interaction.response.edit_message(embed=embed, view=None)
	
	@button(label="Ablehnen", style=discord.ButtonStyle.green)
	async def sdenied(self, interaction: discord.Interaction, button: Button):
		embed = discord.Embed(title="Abgebrochen", description="Shutdown abgebrochen, server läuft noch.", color=discord.Colour.red())
		await interaction.response.edit_message(embed=embed, view=None)