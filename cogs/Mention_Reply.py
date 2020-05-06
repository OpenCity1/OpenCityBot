import discord
from discord.ext import commands


class Mention_Reply(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		if message.channel.type != discord.ChannelType.private:
			for mention in message.mentions:
				if mention == message.guild.me:
					await message.channel.send(f"I am OpenCityBot. My prefix is `{self.bot.command_prefix(self.bot, message)}`. ")
		else:
			for mention in message.mentions:
				if mention == self.bot.user:
					await message.channel.send(f"I am OpenCityBot. My prefix is `{self.bot.prefix_default}`. ")


def setup(bot):
	bot.add_cog(Mention_Reply(bot))
