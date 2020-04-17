__author__ = "Wizard BINAY"

import discord

from discord.ext import commands


class Levelling(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_message(self, message):
		pass

	async def update_data(self, users, user, guild):
		pass

	@commands.command()
	async def level(self, ctx, member: discord.Member):
		pass


def setup(client):
	client.add_cog(Levelling(client))