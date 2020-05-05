import discord
from discord.ext import commands


class Voice_Text_Linking(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
		if after.channel is None:
			pass
		if member.voice.channel is None:
			pass
		if before.channel is None:
			pass


def setup(bot):
	bot.add_cog(Voice_Text_Linking(bot))
