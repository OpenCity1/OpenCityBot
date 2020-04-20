import discord
from discord.ext import commands
import os


class System(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command(help='Pings the bot and gives latency')
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
