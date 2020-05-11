import datetime
import json

import discord
from discord.ext import commands


class Information(commands.Cog):

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

	@commands.command(help='Pings the bot and gives latency')
	async def ping(self, ctx: discord.ext.commands.context.Context):
		time_before = datetime.datetime.utcnow()
		message = await ctx.send(f'Pong! `{round(self.bot.latency * 1000)}ms\\` latency')
		time_after = datetime.datetime.utcnow() - time_before
		await message.edit(content=f"Pong! `{round(self.bot.latency * 1000)}ms\\{round(time_after.total_seconds() * 100)}ms` Latency")

	@commands.command(help="Gives you invite for this bot!")
	async def invite(self, ctx: commands.Context):
		embed = discord.Embed(
			title="Invite Me!",
			color=discord.Colour.gold(),
			description=("This is my invite link. You can use this link to add me to your server!\n"
			             "Link can be found [here](https://discordapp.com/api/oauth2/authorize?client_id=693401671836893235&permissions=8&scope=bot)."
			             )
		)
		await ctx.send(embed=embed)

	@commands.command(help="Gives you the bot's uptime!")
	async def uptime(self, ctx: commands.Context):
		delta_uptime = datetime.datetime.utcnow() - self.bot.start_time
		hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
		minutes, seconds = divmod(remainder, 60)
		days, hours = divmod(hours, 24)
		await ctx.send(f"Uptime: {days}d, {hours}h, {minutes}m, {seconds}s")


def setup(bot):
	bot.add_cog(Information(bot))
