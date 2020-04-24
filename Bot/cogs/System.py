import os

import discord
from discord.ext import commands


class MyHelpCommand(commands.MinimalHelpCommand):
	def get_command_signature(self, command):
		return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)


class System(commands.Cog):

	def __init__(self, client):
		self.client = client
		self._original_help_command = client.help_command
		client.help_command = MyHelpCommand()
		client.help_command.cog = self

	def cog_unload(self):
		self.client.help_command = self._original_help_command

	def send_command_help(self, command):
		pass

	def send_bot_help(self):
		pass

	@commands.command(help='Pings the bot and gives latency')
	@commands.is_owner()
	async def ping(self, ctx: discord.ext.commands.context.Context):
		await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms Latency')

	@commands.command()
	async def load(self, ctx, extension):
		os.chdir("..")
		self.client.load_extension(f'cogs.{extension}')
		await ctx.send(f"Loaded {extension}")

	@commands.command()
	async def unload(self, ctx, extension):
		os.chdir("..")
		self.client.unload_extension(f'cogs.{extension}')
		await ctx.send(f"Unloaded {extension}")

	@commands.command()
	async def reload(self, ctx, extension):
		os.chdir("..")
		self.client.unload_extension(f'cogs.{extension}')
		self.client.load_extension(f'cogs.{extension}')
		await ctx.send(f"Reloaded {extension}")


def setup(client):
	client.add_cog(System(client))
