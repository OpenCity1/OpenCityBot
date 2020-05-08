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
		voice_text_data = json.load(open(self.bot.voice_text_json))[str(member.guild.id)]["voice_text"]

		join_overwrites = {
			member.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, read_message_history=False),
			member: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True)
		}
		leave_overwrites = {
			member.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, read_message_history=False),
			member: discord.PermissionOverwrite(read_messages=False, send_messages=False, read_message_history=False)
		}
		for voice_channel in voice_text_data.keys():
			voice_channel1 = discord.utils.get(member.guild.voice_channels, name=voice_channel)
			if after.channel == voice_channel1 and before.channel is None:
				print(f"{member.display_name} joined {voice_channel1.name}")
				channel: discord.TextChannel = discord.utils.get(member.guild.text_channels, name=voice_text_data[voice_channel])
				await channel.edit(overwrites=join_overwrites)
				break
			if after.channel is None and before.channel == voice_channel1:
				print(f"{member.display_name} left {voice_channel1.name}")
				channel: discord.TextChannel = discord.utils.get(member.guild.text_channels, name=voice_text_data[voice_channel])
				await channel.edit(overwrites=leave_overwrites)
				break
			if member.voice.channel == after.channel:
				pass


def setup(bot):
	bot.add_cog(Voice_Text_Linking(bot))
