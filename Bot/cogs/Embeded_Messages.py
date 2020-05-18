import json
import re

import discord
from discord.ext import commands

from Bot.cogs.utils.timeformat_bot import indian_standard_time_now


class Embeded_Messages(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	async def cog_check(self, ctx):
		if ctx.channel.type == discord.ChannelType.private:
			return True
		if await self.bot.is_owner(ctx.author):
			return True
		guild_data = json.load(open(self.bot.guilds_json))
		enabled = guild_data[str(ctx.guild.id)]["enabled"]
		if f"Bot.cogs.{self.qualified_name}" in enabled:
			return True
		return False

	@commands.command()
	async def test_embed(self, ctx: commands.Context):
		embed = discord.Embed()
		embed.title = f":white_check_mark: You did {re.sub('[0-9]', '', str(ctx.author.name))}"
		embed.colour = discord.Colour.dark_green()
		embed.set_author(name=f"{re.sub('[0-9]', '', str(ctx.author.name))}", icon_url=f"{ctx.author.avatar_url}")
		embed.description = "Trying to find something!"
		embed.set_footer(text=f"{ctx.guild.name} | {indian_standard_time_now()[1]}", icon_url=f"{ctx.guild.icon_url}")
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Embeded_Messages(bot))
