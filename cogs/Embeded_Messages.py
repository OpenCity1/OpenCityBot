import re

import discord
from discord.ext import commands

from cogs.utils.timeformat_bot import get_date_from_short_form_and_unix_time


class Embeded_Messages(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.is_owner()
	async def test_embed(self, ctx: commands.Context):
		embed = discord.Embed()
		embed.title = f":white_check_mark: You did it! {re.sub('[0-9]', '', str(ctx.author.name))}"
		embed.colour = discord.Colour.dark_green()
		embed.set_author(name=f"{re.sub(r'[0-9]', '', str(ctx.author.name))}", icon_url=f"{ctx.author.avatar_url}")
		embed.description = "Trying to find something? Go [here](https://github.com/OpenCity1/OpenCity)"
		embed.set_footer(text=f"{ctx.guild.name} | {get_date_from_short_form_and_unix_time()[1]}", icon_url=f"{ctx.guild.icon_url}")
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Embeded_Messages(bot))
