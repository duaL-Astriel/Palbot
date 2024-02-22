import discord, os, platform, pathlib
from discord.ext import commands
from discord import app_commands

from ..views.sm import ShutdownConfirmationView

class ServerManagementCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def cog_load(self):
		print(f"{self.__class__.__name__}\n----------------------------------------")

	servercommand = app_commands.Group(name="server", description="group of commands to manage Palworld Server")

	@servercommand.command(name="start", description="Start the server")
	async def sstart(self, interaction: discord.Interaction):
		terminal = os.system

		path = str(pathlib.Path(__file__).parents[3])
		if platform.system() == "Windows":
			terminal(path+"/start.bat")

		embed = discord.Embed(title="Erfolgreich", description="Server wurde gestartet!", color=discord.Colour.green())
		await interaction.response.send_message(embed=embed)

	@servercommand.command(name="shutdown", description="shut the server down.")
	async def sshutdown(self, interaction: discord.Interaction, seconds: int=None, message: str=None):
		embed = discord.Embed(title="Bestätigung", description=f"Bist du dir sicher, das du den server {f'in {seconds} sekunden ' if seconds != None else ''}{f'mit der Nachricht {message} ' if message != None else ''}herunterfahren möchtest?", color=discord.Colour.yellow())
		view = ShutdownConfirmationView(seconds, message)
		await interaction.response.send_message(embed=embed, view=view)
		view.message = await interaction.original_response()

async def setup(bot):
	await bot.add_cog(ServerManagementCog(bot))