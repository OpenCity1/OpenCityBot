import os

from discord.ext import commands


class System(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	def cog_check(self, ctx):
		return self.bot.is_owner(ctx.author)

	@commands.command(help="Loads an extension", hidden=True)
	async def load(self, ctx, extension):
		os.chdir("..")
		self.bot.load_extension(f'cogs.{extension}')
		await ctx.send(f"Loaded {extension}")

	@commands.command(help="Unloads an extension", hidden=True)
	async def unload(self, ctx, extension):
		os.chdir("..")
		self.bot.unload_extension(f'cogs.{extension}')
		await ctx.send(f"Unloaded {extension}")

	@commands.command(help="Reloads an extension", hidden=True)
	async def reload(self, ctx, extension):
		os.chdir("..")
		self.bot.unload_extension(f'cogs.{extension}')
		self.bot.load_extension(f'cogs.{extension}')
		await ctx.send(f"Reloaded {extension}")

	@commands.command(hidden=True)
	async def leave_server(self, ctx: commands.Context):
		await ctx.guild.leave()


def setup(bot):
	bot.add_cog(System(bot))
