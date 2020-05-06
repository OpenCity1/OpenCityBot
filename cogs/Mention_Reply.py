import random

import discord
from discord.ext import commands


class Mention_Reply(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		prefix = random.choice(self.bot.command_prefix(self.bot, message))
		for mention in message.mentions:
			if mention == self.bot.user:
				await message.channel.send(f"I am OpenCityBot. To see my prefix do `{prefix}prefix`. ")


def setup(bot):
	bot.add_cog(Mention_Reply(bot))
