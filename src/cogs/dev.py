import discord
from discord.ext import commands

from ..lib.bot import PalBot

class DevCog(commands.Cog):
	def __init__(self, bot: PalBot):
		self.bot = bot
	
	async def cog_load(self):
		print(f"{self.__class__.__name__}\n----------------------------------------")
		print(f"To refresh application commands, use {self.bot.command_prefix}sync")
	
	@commands.command(name="sync")
	async def csync(self, ctx: commands.Context):
		synced = await self.bot.tree.sync()
		await ctx.send(embed=discord.Embed(title="Success", description=f"synced {len(synced)} commands", color=discord.Colour.green()))
	

async def setup(bot):
	await bot.add_cog(DevCog(bot))