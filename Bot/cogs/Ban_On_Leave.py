import datetime

import discord
from discord.ext import commands


class Ban_On_Leave(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_member_remove(self, member: discord.Member):
		print("Working")
		async for entry in member.guild.audit_logs(action=discord.AuditLogAction.kick, limit=1):
			if (datetime.datetime.utcnow() - entry.created_at).total_seconds() < 20:
				if entry.target == member:
					return
		await member.ban()


def setup(client):
	client.add_cog(Ban_On_Leave(client))
