import json

import discord
from discord.ext import commands


class Test_Cog(commands.Cog):

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

	@commands.command()
	async def test(self, ctx):
		await ctx.send("It worked!")


def setup(bot):
	bot.add_cog(Test_Cog(bot))
