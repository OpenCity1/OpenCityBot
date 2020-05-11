__author__ = "Sairam"
import json
from typing import Optional

import discord
from discord.ext import commands


class Moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.suggestion_number = 0
		self.report_number = 0

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

	@commands.command(help='Bans the given user')
	@commands.has_guild_permissions(ban_members=True)
	async def ban(self, ctx: discord.ext.commands.context.Context, member: discord.Member, *, reason="No reason provided"):
		role = discord.utils.get(ctx.guild.roles, name='Banned Members')
		await member.add_roles(role, reason=reason)
		await ctx.send(f'{member} is banned because of {reason}.')

	@commands.command(help='Kicks the given user')
	@commands.has_guild_permissions(kick_members=True)
	async def kick(self, ctx: discord.ext.commands.context.Context, member: discord.Member, *, reason="No reason provided"):
		role = discord.utils.get(ctx.guild.roles, name='Kicked Members')
		await member.add_roles(role, reason=reason)
		await ctx.send(f'{member} is kicked because of {reason}.')

	@commands.command(help="Mutes the given user")
	@commands.has_guild_permissions(manage_roles=True)
	async def mute(self, ctx: discord.ext.commands.context.Context, member: discord.Member, *, reason="No reason provided"):
		role = discord.utils.get(ctx.guild.roles, name='Muted Members')
		await member.add_roles(role, reason=reason)
		await ctx.send(f"{member} is muted because of {reason}.")

	@commands.command(help="Unmutes the given user")
	@commands.has_guild_permissions(manage_roles=True)
	async def unmute(self, ctx: discord.ext.commands.context.Context, member: discord.Member, *, reason="No reason provided"):
		role = discord.utils.get(ctx.guild.roles, name='Muted Members')
		await member.remove_roles(role, reason=reason)
		await ctx.send(f"{member} is unmuted because of {reason}.")

	@commands.command(help='Unbans the given user')
	@commands.has_guild_permissions(ban_members=True)
	async def unban(self, ctx: discord.ext.commands.context.Context, member: discord.Member, *, reason="No reason provided"):
		role = discord.utils.get(ctx.guild.roles, name='Banned Members')
		await member.remove_roles(role, reason=reason)
		await ctx.send(f'{member} is unbanned because of {reason}.')

	@commands.command(help='Unkicks the given user')
	@commands.has_guild_permissions(kick_members=True)
	async def unkick(self, ctx: discord.ext.commands.context.Context, member: discord.Member, *, reason="No reason provided"):
		role = discord.utils.get(ctx.guild.roles, name='Kicked Members')
		await member.remove_roles(role, reason=reason)
		await ctx.send(f'{member} is unkicked because of {reason}.')

	@commands.command(help="Purges the given amount of messages", aliases=['clear'])
	@commands.has_guild_permissions(manage_messages=True)
	async def purge(self, ctx: discord.ext.commands.context.Context, amount_of_messages=1, author: Optional[discord.Member] = None):
		await ctx.channel.purge(limit=amount_of_messages, check=lambda m: True if author is None else m.author == author)

	@commands.command(help="Get the status!")
	async def status(self, ctx: commands.Context, member: discord.Member):
		await ctx.send(member.activity)


# @commands.command()
# async def status(self, ctx: commands.Context, member: discord.Member):
# 	await ctx.send(member.activity)


def setup(bot):
	bot.add_cog(Moderation(bot))
