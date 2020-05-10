import json
from typing import Optional

import discord
from discord.ext import commands

from cogs.utils.timeformat_bot import get_date_from_short_form_and_unix_time


class Suggestions(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	def cog_check(self, ctx):
		if ctx.channel.type == discord.ChannelType.private:
			return True
		guild_data = json.load(open(self.bot.guilds_json))
		enabled = guild_data[str(ctx.guild.id)]["enabled"]
		if f"cogs.{ctx.cog.qualified_name}" in enabled:
			return True
		return False

	@commands.group(help="Suggest something!", invoke_without_command=True)
	async def suggest(self, ctx: commands.Context, type1, *, suggestion):
		counts = json.load(open(self.bot.counts_json))
		if "suggestion_count" not in counts.keys():
			counts["suggestion_count"] = self.bot.start_number
		if "suggestion_number" not in counts.keys():
			counts["suggestion_number"] = 1
		title = f"Suggestion #{counts['suggestion_number']}"
		embed = discord.Embed(
			title=title,
			description=(
				f"**Suggestion**: {suggestion}\n"
				f"**Suggestion by**: {ctx.author.mention}"
			),
			color=discord.Colour.green()
		).set_footer(text=f"SuggestionID: {counts['suggestion_count']} | {get_date_from_short_form_and_unix_time()[1]}")
		embed.set_author(name=f"{ctx.author.name}", icon_url=f"{ctx.author.avatar_url}")
		message_sent = await ctx.send(embed=embed)
		await message_sent.add_reaction(f":_tick:705003237174018179")
		await message_sent.add_reaction(f":_neutral:705003236687609936")
		await message_sent.add_reaction(f":_cross:705003237174018158")
		await message_sent.add_reaction(f":_already_there:705003236897194004")
		suggestions = json.load(open(self.bot.suggestions_json))
		if "suggestions" not in suggestions.keys():
			suggestions["suggestions"] = []
		suggestion_1 = {
			"suggestionID": counts["suggestion_count"],
			"suggestionMessageID": message_sent.id,
			"suggestionTitle": title,
			"suggestionContent": suggestion,
			"suggestionAuthor": f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})",
			"suggestionType": f"{type1}",
			"suggestionStatus": "waiting"
		}
		counts["suggestion_count"] += 1
		counts["suggestion_number"] += 1
		json.dump(counts, open(self.bot.counts_json, "w+"), indent='\t')
		suggestions["suggestions"].append(suggestion_1)
		json.dump(suggestions, open(self.bot.suggestions_json, "w+"), indent='\t')
		await ctx.author.send("Your suggestion is sent!, This is how your suggestion look like!", embed=embed)

	@suggest.command(name="approve")
	async def suggest_approve(self, ctx: commands.Context, suggestion_id: int, *, reason: Optional[str] = None):
		suggestions = json.load(open(self.bot.suggestions_json))
		for suggestion in suggestions["suggestions"]:
			if suggestion['suggestionID'] == suggestion_id:
				embed = discord.Embed()
				author = ctx.guild.get_member(int(suggestion['suggestionAuthor'].split(' ')[1].strip('( )')))
				embed.title = suggestion['suggestionTitle'] + " Approved"
				embed.description = (
					f"**Suggestion**: {suggestion['suggestionContent']}\n"
					f"**Suggested by**: {author.mention}"
				)
				if reason:
					embed.add_field(name=f"Reason by {suggestion['suggestionAuthor'].split(' ')[0]}", value=reason)
				embed.set_author(name=author.name, icon_url=author.avatar_url)
				embed.colour = discord.Colour.dark_green()
				message_ge = await ctx.channel.fetch_message(suggestion["suggestionMessageID"])
				await message_ge.edit(embed=embed)
				suggestion['suggestionStatus'] = "approved"

		json.dump(suggestions, open(self.bot.suggestions_json, "w+"), indent='\t')

	@suggest.command(name="deny")
	async def suggest_deny(self, ctx: commands.Context, suggestion_id, *, reason: Optional[str] = None):
		suggestions = json.load(open(self.bot.suggestions_json))
		for suggestion in suggestions["suggestions"]:
			if int(suggestion['suggestionID']) == suggestion_id:
				embed = discord.Embed()
				author = ctx.guild.get_member(suggestion['suggestionAuthor'].split(' ')[1].strip('( )'))
				embed.title = suggestion['suggestionTitle'] + " Denied"
				embed.description = (
					f"**Suggestion**: {suggestion['suggestionContent']}\n"
					f"**Suggested by**: {author.mention}"
				)
				if reason:
					embed.add_field(name=f"Reason by {suggestion['suggestionAuthor'].split(' ')[0]}", value=reason)
				embed.set_author(name=author.name, icon_url=author.avatar_url)
				embed.colour = discord.Colour.blue()
				message_ge: discord.Message = await ctx.channel.fetch_message(suggestion["suggestionMessageID"])
				await message_ge.edit(embed=embed)
				suggestion['suggestionStatus'] = "denied"

		json.dump(suggestions, open(self.bot.suggestions_json, "w+"), indent='\t')

	@suggest.command(name="consider")
	async def suggest_consider(self, ctx: commands.Context, suggestion_id, *, reason: Optional[str] = None):
		suggestions = json.load(open(self.bot.suggestions_json))
		for suggestion in suggestions["suggestions"]:
			if suggestion['suggestionID'] == suggestion_id:
				embed = discord.Embed()
				author = ctx.guild.get_member(suggestion['suggestionAuthor'].split(' ')[1].strip('( )'))
				embed.title = suggestion['suggestionTitle'] + " Considered"
				embed.description = (
					f"**Suggestion**: {suggestion['suggestionContent']}\n"
					f"**Suggested by**: {author.mention}"
				)
				if reason:
					embed.add_field(name=f"Reason by {suggestion['suggestionAuthor'].split(' ')[0]}", value=reason)
				embed.set_author(name=author.name, icon_url=author.avatar_url)
				embed.colour = discord.Colour.dark_red()
				message_ge: discord.Message = await ctx.channel.fetch_message(suggestion["suggestionMessageID"])
				await message_ge.edit(embed=embed)
				suggestion['suggestionStatus'] = "considered"

		json.dump(suggestions, open(self.bot.suggestions_json, "w+"), indent='\t')

	@suggest.command(name="implemented")
	async def suggest_implemented(self, ctx: commands.Context, suggestion_id, *, reason: Optional[str] = None):
		suggestions = json.load(open(self.bot.suggestions_json))
		for suggestion in suggestions["suggestions"]:
			if suggestion['suggestionID'] == suggestion_id:
				embed = discord.Embed()
				author = ctx.guild.get_member(suggestion['suggestionAuthor'].split(' ')[1].strip('( )'))
				embed.title = suggestion['suggestionTitle'] + " Implemented"
				embed.description = (
					f"**Suggestion**: {suggestion['suggestionContent']}\n"
					f"**Suggested by**: {author.mention}"
				)
				if reason:
					embed.add_field(name=f"Reason by {suggestion['suggestionAuthor'].split(' ')[0]}", value=reason)
				embed.set_author(name=author.name, icon_url=author.avatar_url)
				embed.colour = discord.Colour(0x00ffff)
				message_ge: discord.Message = await ctx.channel.fetch_message(suggestion["suggestionMessageID"])
				await message_ge.edit(embed=embed)
				suggestion['suggestionStatus'] = "implemented"

		json.dump(suggestions, open(self.bot.suggestions_json, "w+"), indent='\t')


def setup(bot):
	bot.add_cog(Suggestions(bot))
