__author__ = "Sairam"

from typing import Optional

import discord
from discord.ext import commands

from timeformat_bot import get_date_from_short_form_and_unix_time


class Moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.suggestion_number = 0
		self.report_number = 0

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
		await member.remove_roles(role, reason=reason)
		await ctx.send(f'{member} is unbanned because of {reason}.')

	@commands.command(help='Unkicks the given user')
	async def unkick(self, ctx: discord.ext.commands.context.Context, member: discord.Member, *, reason="No reason provided"):
		role = discord.utils.get(ctx.guild.roles, name='Kicked Members')
		await member.remove_roles(role, reason=reason)
		await ctx.send(f'{member} is unkicked because of {reason}.')

	@commands.command(help="Purges the given amount of messages", aliases=['clear'])
<<<<<<< HEAD:cogs/Moderation.py
	async def purge(self, ctx: discord.ext.commands.context.Context, amount_of_messages=1, author: Optional[discord.Member] = None):
		await ctx.channel.purge(limit=amount_of_messages, check=lambda m: True if author is None else m.author == author)

	@commands.command()
	async def status(self, ctx: commands.Context, member: discord.Member):
		await ctx.send(member.activity)

	@commands.command()
	async def suggest(self, ctx: commands.Context, *, suggestion):
		embed = discord.Embed(
			title=f"Suggestion #{self.suggestion_number}",
			description=(
				f"**Suggestion**: {suggestion}\n"
				f"**Suggestion by**: {ctx.author.mention}"
			),
			color=discord.Colour.green()
		).set_footer(text=f"SuggestionID: {ctx.message.id} | {get_date_from_short_form_and_unix_time()[1]}").set_author(name=f"{ctx.author.name}",
		                                                                                                                icon_url=f"{ctx.author.avatar_url}")
		message_sent = await ctx.send(embed=embed)
		await message_sent.add_reaction(f":_tick:705003237174018179")
		await message_sent.add_reaction(f":_neutral:705003236687609936")
		await message_sent.add_reaction(f":_cross:705003237174018158")
		await message_sent.add_reaction(f":_already_there:705003236897194004")
		self.suggestion_number += 1

	@commands.command()
	async def report(self, ctx: commands.Context, user: discord.Member, *, reason):
		embed = discord.Embed(
			title=f"Report #{self.report_number}",
			description=(
				f"**Reported User**: {user.mention}\n"
				f"**Reported Reason**: {reason}\n"
				f"**Reported by**: {ctx.author.mention}"
			),
			color=discord.Colour.blurple()
		).set_footer(text=f"ReportID: {ctx.message.id} | {get_date_from_short_form_and_unix_time()[1]}").set_author(name=f"{ctx.author.name}", icon_url=f"{ctx.author.avatar_url}")
		message_sent = await ctx.send(embed=embed)
		await message_sent.add_reaction(f":_tick:705003237174018179")
		await message_sent.add_reaction(f":_neutral:705003236687609936")
		await message_sent.add_reaction(f":_cross:705003237174018158")
		self.report_number += 1
=======
	async def purge(self, ctx: discord.ext.commands.context.Context, amount_of_messages=0):
		await ctx.channel.purge(limit=amount_of_messages)
>>>>>>> master:Bot/cogs/Moderation.py

	@commands.command()
	async def status(self, ctx: commands.Context, member: discord.Member):
		await ctx.send(member.activity)


def setup(bot):
	bot.add_cog(Moderation(bot))
