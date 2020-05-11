import json

import discord
from discord.ext import commands


class Roles(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	async def cog_check(self, ctx):
		if ctx.channel.type == discord.ChannelType.private:
			return True
		if await self.bot.is_owner(ctx.author):
			return True
		guild_data = json.load(open(self.bot.guilds_json))
		enabled = guild_data[str(ctx.guild.id)]["enabled"]
		if f"cogs.{ctx.cog.qualified_name}" in enabled:
			return True
		return False

	@commands.group(name="role")
	async def _role(self, ctx: commands.Context):
		pass

	@_role.command()
	async def something(self, ctx: commands.Context):
		pass


def setup(bot):
	bot.add_cog(Roles(bot))
