import json
import random

import discord
from discord.ext import commands


class Mention_Reply(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	def cog_check(self, ctx):
		guild_data = json.load(open(self.bot.guilds_json))
		enabled = guild_data[str(ctx.guild.id)]["enabled"]
		if f"cogs.{ctx.cog.qualified_name}" in enabled:
			return True
		return False

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		prefix = random.choice(self.bot.command_prefix(self.bot, message))
		if message.content.startswith('<@'):
			for mention in message.mentions:
				if mention == self.bot.user:
					await message.channel.send(f"I am OpenCityBot. To see my prefix do `{prefix}prefix`. ")


def setup(bot):
	bot.add_cog(Mention_Reply(bot))
