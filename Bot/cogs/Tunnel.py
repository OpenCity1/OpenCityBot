import json

import discord
from discord.ext import commands


class Tunnel(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	def cog_check(self, ctx):
		if ctx.channel.type == discord.ChannelType.private:
			return True
		guild_data = json.load(open(self.bot.guilds_json))
		enabled = guild_data[str(ctx.guild.id)]["enabled"]
		if f"cogs.{ctx.cog.qualified_name}" in enabled:
			return True
		return False

	@commands.group()
	async def tunnel(self, ctx: commands.Context):
		pass


def setup(bot):
	bot.add_cog(Tunnel(bot))
