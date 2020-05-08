import json

import discord
from discord.ext import commands


class Voice_Text_Linking(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	def cog_check(self, ctx):
		guild_data = json.load(open(self.bot.guilds_json))
		enabled = guild_data[str(ctx.guild.id)]["enabled"]
		if f"cogs.{ctx.cog.qualified_name}" in enabled:
			return True
		return False

	@commands.Cog.listener()
	async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
		# if after.channel is None:
		# 	pass
		# if member.voice.channel is None:
		# 	pass
		# if before.channel is None:
		# 	pass
		pass


def setup(bot):
	bot.add_cog(Voice_Text_Linking(bot))
