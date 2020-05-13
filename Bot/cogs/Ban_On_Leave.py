import datetime
import json

import discord
from discord.ext import commands


class Ban_On_Leave(commands.Cog):

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
	async def on_member_remove(self, member: discord.Member):
		guild_data = json.load(open(self.bot.guilds_json))
		enabled = guild_data[str(member.guild.id)]["enabled"]
		if f"cogs.{self.qualified_name}" in enabled:
			async for entry in member.guild.audit_logs(action=discord.AuditLogAction.kick):
				if (datetime.datetime.utcnow() - entry.created_at).total_seconds() < 20:
					if entry.target == member:
						return
			await member.ban()


def setup(bot):
	bot.add_cog(Ban_On_Leave(bot))
