import os

import discord
from discord.ext import commands


class MyHelpCommand(commands.MinimalHelpCommand):
	def get_command_signature(self, command):
		return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)


class System(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self._original_help_command = bot.help_command
		bot.help_command = MyHelpCommand()
		bot.help_command.cog = self

	def cog_unload(self):
		self.bot.help_command = self._original_help_command

	def send_command_help(self, command):
		pass

	def send_bot_help(self):
		pass

	@commands.command(help='Pings the bot and gives latency')
	async def ping(self, ctx: discord.ext.commands.context.Context):
		await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms Latency')

	@commands.command()
	@commands.is_owner()
	async def load(self, ctx, extension):
		os.chdir("..")
		self.bot.load_extension(f'cogs.{extension}')
		await ctx.send(f"Loaded {extension}")

	@commands.command()
	@commands.is_owner()
	async def unload(self, ctx, extension):
		os.chdir("..")
		self.bot.unload_extension(f'cogs.{extension}')
		await ctx.send(f"Unloaded {extension}")

	@commands.command()
	@commands.is_owner()
	async def reload(self, ctx, extension):
		os.chdir("..")
		self.bot.unload_extension(f'cogs.{extension}')
		self.bot.load_extension(f'cogs.{extension}')
		await ctx.send(f"Reloaded {extension}")


def setup(bot):
	bot.add_cog(System(bot))
