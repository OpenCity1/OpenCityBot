__author__ = "Wizard BINAY"

import discord

from discord.ext import commands


class Leveling(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.user_xps = 1025

	@commands.Cog.listener()
	async def on_message(self, message):
		pass

	async def update_data(self, users, user, guild):
		pass

	@commands.command()
	async def level(self, ctx, member: discord.Member):
		if discord.utils.find(lambda r: r.name == 'Respected People', member.guild.roles) in member.roles:
			await ctx.send(f"<@{member.id}> you are a Respected People or you have finished leveling")
		else:
			await ctx.send(f"<@{member.id}> you have {self.user_xps}xps!")


def setup(client):
	client.add_cog(Leveling(client))