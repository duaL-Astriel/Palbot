import discord, asyncio
from discord.ui import View, Button, button
from rcon.source import Client
from ..lib.bot import PalBot

class ShutdownConfirmationView(View):
	def __init__(self, seconds: int=None, message=None):
		self.seconds = seconds
		self.msg = message
		self.bot = PalBot()
		super().__init__(timeout=30)
	
	@button(label="Bestätigen", style=discord.ButtonStyle.green)
	async def sconfirmation(self, interaction: discord.Interaction, button: Button):
		
		if self.seconds != None:
			with Client(host=self.bot.pwhost, port=self.bot.pwport, passwd=self.bot.pwpasswrd) as client:
				# response = await client.run("Shutdown %d %s", self.seconds, self.msg)
				response = await client.run(command="shutdown")
			print(response)
			# await Client("shutdown", host=self.bot.pwhost, port=self.bot.pwport, passwd=self.bot.pwpasswrd)
			embed = discord.Embed(title="Erfolgreich", description="Server wurde erfolgreich heruntergefahren")
			await interaction.response.edit_message(embed=embed, view=None)
		else: 
			with Client(host=self.bot.pwhost, port=self.bot.pwport, passwd=self.bot.pwpasswrd) as client:
				response = await client.run(command="shutdown")
				embed = discord.Embed(title="Erfolgreich", description="Server wurde erfolgreich heruntergefahren.")
				await interaction.response.edit_message(embed=embed, view=None)
				print(response)
	
	@button(label="Abbrechen", style=discord.ButtonStyle.danger)
	async def sdenied(self, interaction: discord.Interaction, button: Button):
		embed = discord.Embed(title="Abgebrochen", description="Shutdown vom Benutzer abgebrochen.")
		await interaction.response.edit_message(embed=embed, view=None)