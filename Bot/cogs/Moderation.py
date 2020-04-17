__author__ = "Sairam"

import discord

from discord.ext import commands


class Moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(help='Bans the given user')
	async def ban(self, ctx: discord.ext.commands.context.Context, member: discord.Member, *, reason="No reason provided"):
		role = discord.utils.get(ctx.guild.roles, name='Banned Members')
		await member.add_roles(role, reason=reason)
		await ctx.send(f'{member} is banned because of {reason}.')

	@commands.command(help='Kicks the given user')
	async def kick(self, ctx: discord.ext.commands.context.Context, member: discord.Member, *, reason="No reason provided"):
		role = discord.utils.get(ctx.guild.roles, name='Kicked Members')
		await member.add_roles(role, reason=reason)
		await ctx.send(f'{member} is kicked because of {reason}.')

	@commands.command(help="Mutes the given user")
	async def mute(self, ctx: discord.ext.commands.context.Context, member: discord.Member, *, reason="No reason provided"):
		role = discord.utils.get(ctx.guild.roles, name='Muted Members')
		await member.add_roles(role, reason=reason)
		await ctx.send(f"{member} is muted because of {reason}.")

	@commands.command(help="Unmutes the given user")
	async def unmute(self, ctx: discord.ext.commands.context.Context, member: discord.Member, *, reason="No reason provided"):
		role = discord.utils.get(ctx.guild.roles, name='Muted Members')
		await member.remove_roles(role, reason=reason)
		await ctx.send(f"{member} is unmuted because of {reason}.")

	@commands.command(help='Unbans the given user')
	async def unban(self, ctx: discord.ext.commands.context.Context, member: discord.Member, *, reason="No reason provided"):
		role = discord.utils.get(ctx.guild.roles, name='Banned Members')
		print(role)
		await member.remove_roles(role, reason=reason)
		await ctx.send(f'{member} is unbanned because of {reason}.')

	@commands.command(help='Unkicks the given user')
	async def unkick(self, ctx: discord.ext.commands.context.Context, member: discord.Member, *, reason="No reason provided"):
		role = discord.utils.get(ctx.guild.roles, name='Kicked Members')
		await member.remove_roles(role, reason=reason)
		await ctx.send(f'{member} is unkicked because of {reason}.')

	@commands.command(help="Purges the given amount of messages")
	async def purge(self, ctx: discord.ext.commands.context.Context, amount_of_messages=0):
		await ctx.channel.purge(limit=amount_of_messages)


def setup(bot):
	bot.add_cog(Moderation(bot))
