import json

import discord
from discord.ext import commands

from Bot.cogs.utils.timeformat_bot import get_date_from_short_form_and_unix_time


class Reports(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	async def cog_check(self, ctx):
		if ctx.channel.type == discord.ChannelType.private:
			return True
		if await self.bot.is_owner(ctx.author):
			return True
		guild_data = json.load(open(self.bot.guilds_json))
		enabled = guild_data[str(ctx.guild.id)]["enabled"]
		if f"Bot.cogs.{ctx.cog.qualified_name}" in enabled:
			return True
		return False

	@commands.group(help="Reports a user with reason!", invoke_without_command=True)
	async def report(self, ctx: commands.Context, user: discord.Member, *, reason="No reason given!"):
		counts = json.load(open(self.bot.counts_json))
		if "id" not in counts.keys():
			counts["id"] = {}
		if str(ctx.guild.id) not in counts.keys():
			counts[str(ctx.guild.id)] = {}
		if "report_id" not in counts["id"].keys():
			counts["id"]["report_id"] = self.bot.start_number
		if "report_number" not in counts[str(ctx.guild.id)].keys():
			counts[str(ctx.guild.id)]["report_number"] = 1
		title = f"""Report #{counts[str(ctx.guild.id)]["report_number"]}"""
		embed = discord.Embed(
			title=title,
			description=(
				f"**Reported User**: {user.mention}\n"
				f"**Reported Reason**: {reason}\n"
				f"**Reported by**: {ctx.author.mention}"
			),
			color=discord.Colour.blurple()
		)
		embed.set_footer(text=f"""ReportID: {counts["id"]["report_id"]} | {get_date_from_short_form_and_unix_time()[1]}""")
		embed.set_author(name=f"{ctx.author.name}", icon_url=f"{ctx.author.avatar_url}")
		message_sent = await ctx.send(embed=embed)
		await message_sent.add_reaction(f":_tick:705003237174018179")
		await message_sent.add_reaction(f":_neutral:705003236687609936")
		await message_sent.add_reaction(f":_cross:705003237174018158")
		reports = json.load(open(self.bot.reports_json))
		if "reports" not in reports.keys():
			reports["reports"] = []
		report_1 = {
			"reportID": counts['id']["report_id"],
			"reportMessageID": message_sent.id,
			"reportTitle": title,
			"reportReason": reason,
			"reportAuthor": f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})",
			"reportTime": get_date_from_short_form_and_unix_time()[1],
			"reportStatus": "waiting",
			"reportUser": f"{user.name}#{user.discriminator} ({user.id})"
		}
		reports["reports"].append(report_1)
		counts['id']["report_id"] += 1
		counts[str(ctx.guild.id)]["report_number"] += 1

		json.dump(reports, open(self.bot.reports_json, "w"), indent='\t')
		json.dump(counts, open(self.bot.counts_json, "w"), indent='\t')

		await ctx.author.send("Your report successfully sent!, this is how it would look like", embed=embed)

	@report.command(name="accept", help="Accepts a report")
	async def report_accept(self, ctx: commands.Context, report_id: int, *, reason):
		reports = json.load(open(self.bot.reports_json))
		for report in reports["reports"]:
			if int(report["reportID"]) == report_id:
				embed = discord.Embed()
				author = ctx.guild.get_member(int(report['reportAuthor'].split(' ')[-1].strip('( )')))
				embed.title = report['reportTitle'] + " Accepted"
				report_user = ctx.guild.get_member(int(report['reportUser'].split(' ')[-1].strip('( )')))
				embed.description = (
					f"**Reported User**: {report_user.mention}\n"
					f"**Reported Reason**: {report['reportReason']}\n"
					f"**Reported by**: {author.mention}"
				)
				if reason:
					embed.add_field(name=f"Reason by {report['reportAuthor'].split(' ')[0]}", value=reason)
				embed.set_author(name=author.name, icon_url=author.avatar_url)
				embed.colour = discord.Colour.dark_green()
				embed.set_footer(text=f"ReportID: {report['reportID']} | {report['reportTime']}")
				message_ge = await ctx.channel.fetch_message(report["reportMessageID"])
				await message_ge.edit(embed=embed)
				report['reportStatus'] = "accepted"

		json.dump(reports, open(self.bot.reports_json, "w+"), indent='\t')

	@report.command(name="decline", help="Declines a report")
	async def report_decline(self, ctx: commands.Context, report_id: int, *, reason):
		reports = json.load(open(self.bot.reports_json))
		for report in reports["reports"]:
			if int(report["reportID"]) == report_id:
				embed = discord.Embed()
				author = ctx.guild.get_member(int(report['reportAuthor'].split(' ')[-1].strip('( )')))
				embed.title = report['reportTitle'] + " Declined"
				report_user = ctx.guild.get_member(int(report['reportUser'].split(' ')[-1].strip('( )')))
				embed.description = (
					f"**Reported User**: {report_user.mention}\n"
					f"**Reported Reason**: {report['reportReason']}\n"
					f"**Reported by**: {author.mention}"
				)
				if reason:
					embed.add_field(name=f"Reason by {report['reportAuthor'].split(' ')[0]}", value=reason)
				embed.set_author(name=author.name, icon_url=author.avatar_url)
				embed.colour = discord.Colour.dark_red()
				embed.set_footer(text=f"ReportID: {report['reportID']} | {report['reportTime']}")
				message_ge = await ctx.channel.fetch_message(report["reportMessageID"])
				await message_ge.edit(embed=embed)
				report['reportStatus'] = "declined"

		json.dump(reports, open(self.bot.reports_json, "w+"), indent='\t')


def setup(bot):
	bot.add_cog(Reports(bot))
