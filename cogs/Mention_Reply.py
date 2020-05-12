import json
import random

import discord
from discord.ext import commands


class Mention_Reply(commands.Cog):

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

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		try:
			prefix = random.choice(self.bot.command_prefix(self.bot, message))
			guild_data = json.load(open(self.bot.guilds_json))
			enabled = guild_data[str(message.guild.id)]["enabled"]
			if message.channel.type == discord.ChannelType.private or f"cogs.{self.qualified_name}" in enabled:
				if message.content.startswith('<@'):
					for mention in message.mentions:
						if mention == self.bot.user:
							await message.channel.send(f"I am OpenCityBot. To see my prefix do `{prefix}prefix`. ")
							return
		except AttributeError:
			pass


def setup(bot):
	bot.add_cog(Mention_Reply(bot))
