import json
from io import BytesIO
from typing import Optional

import discord
from discord.ext import commands

from cogs.utils.timeformat_bot import get_date_from_short_form_and_unix_time


class Ticket(commands.Cog):
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

	@commands.group()
	async def ticket(self, ctx: commands.Context):
		pass

	@ticket.command(name="new")
	async def ticket_new(self, ctx: commands.Context, *, reason: Optional[str]):
		counts = json.load(open(self.bot.counts_json))
		if "id" not in counts.keys():
			counts["id"] = {}
		if str(ctx.guild.id) not in counts.keys():
			counts[str(ctx.guild.id)] = {}
		if "ticket_id" not in counts["id"].keys():
			counts["id"]["ticket_id"] = self.bot.start_number
		if "ticket_number" not in counts[str(ctx.guild.id)].keys():
			counts[str(ctx.guild.id)]["ticket_number"] = 1
		support_role = discord.utils.find(lambda r: r.name == "Support", ctx.guild.roles)
		if support_role is None:
			await ctx.guild.create_role(name="Support")
		overwrites = {
			ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
			ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True),
			support_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True)
		}
		embed = discord.Embed(
			title=f"Thank you for creating a ticket! {ctx.author.name} This is Ticket #{counts[str(ctx.guild.id)]['ticket_number']}",
			description=f"Thank you for creating a ticket! {ctx.author.mention}\nWe'll get back to you as soon as possible.",
		)
		embed.set_footer(text=f"TicketID: {counts['id']['ticket_id']} | {get_date_from_short_form_and_unix_time()[1]}")
		if discord.utils.get(ctx.guild.categories, name="Support") not in ctx.guild.categories:
			await ctx.guild.create_category(name="Support")
		channel = await ctx.guild.create_text_channel(name=f'{ctx.author.name}-{ctx.author.discriminator}', category=discord.utils.get(ctx.guild.categories, name="Support"),
		                                              overwrites=overwrites)
		await channel.edit(topic=f"Opened by {ctx.author.name} - All messages sent to this channel are being recorded.")
		await channel.send(embed=embed)
		tickets_data = json.load(open(self.bot.tickets_json))
		if "tickets" not in tickets_data.keys():
			tickets_data["tickets"] = []

		ticket_1 = {
			"ticketID": counts['id']["ticket_id"],
			"ticketAuthor": f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})",
			"ticketOpenedTime": get_date_from_short_form_and_unix_time()[1],
			"ticketClosedTime": "Not closed till now!",
			"ticketGuildID": f"{ctx.guild.id}",
			"ticketReason": f"{reason}",
			"ticketStatus": "opened"
		}
		tickets_data["tickets"].append(ticket_1)
		counts[str(ctx.guild.id)]["ticket_number"] += 1
		counts["id"]["ticket_id"] += 1
		json.dump(counts, open(self.bot.counts_json, "w"), indent='\t')
		json.dump(tickets_data, open(self.bot.tickets_json, 'w'), indent='\t')

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		guild: discord.Guild = self.bot.get_guild(payload.guild_id)
		guild_data = json.load(open(self.bot.guilds_json))
		enabled = guild_data[str(guild.id)]["enabled"]
		if f"cogs.{self.qualified_name}" in enabled:
			counts = json.load(open(self.bot.counts_json))
			if "id" not in counts.keys():
				counts["id"] = {}
			if str(guild.id) not in counts.keys():
				counts[str(guild.id)] = {}
			if "ticket_id" not in counts["id"].keys():
				counts["id"]["ticket_id"] = self.bot.start_number
			if "ticket_number" not in counts[str(guild.id)].keys():
				counts[str(guild.id)]["ticket_number"] = 1
			tickets_data = json.load(open(self.bot.tickets_json))
			if str(guild.id) not in tickets_data:
				tickets_data[str(guild.id)] = {}
				tickets_data[str(guild.id)]['ticket_emoji'] = []
			emoji = payload.emoji
			support_role = discord.utils.find(lambda r: r.name == "Support", guild.roles)
			if support_role is None:
				await guild.create_role(name="Support")
			overwrites = {
				guild.default_role: discord.PermissionOverwrite(read_messages=False),
				guild.get_member(payload.user_id): discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True),
				support_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True)
			}
			user: discord.Member = guild.get_member(payload.user_id)
			embed = discord.Embed(
				title=f"Thank you for creating a ticket! {user.name} This is Ticket #{counts[str(guild.id)]['ticket_number']}",
				description=f"Thank you for creating a ticket! {user.mention}\nWe'll get back to you as soon as possible.",
			)
			embed.set_footer(text=f"TicketID: {counts['id']['ticket_id']} | {get_date_from_short_form_and_unix_time()[1]}")
			for emoji_2 in tickets_data[str(guild.id)]['ticket_emoji']:
				if str(emoji) == str(emoji_2):
					if discord.utils.get(guild.categories, name="Support") not in guild.categories:
						await guild.create_category(name="Support")
					channel = await guild.create_text_channel(name=f'{user.name}-{user.discriminator}', category=discord.utils.get(user.guild.categories, name="Support"),
					                                          overwrites=overwrites)
					await channel.edit(topic=f"Opened by {user.name} - All messages sent to this channel are being recorded.")
					await channel.send(embed=embed)
				tickets_data = json.load(open(self.bot.tickets_json))
				if "tickets" not in tickets_data.keys():
					tickets_data["tickets"] = []

				ticket_1 = {
					"ticketID": counts['id']["ticket_id"],
					"ticketAuthor": f"{user.name}#{user.discriminator} ({user.id})",
					"ticketOpenedTime": get_date_from_short_form_and_unix_time()[1],
					"ticketClosedTime": "Not closed till now!",
					"ticketGuildID": f"{guild.id}",
					"ticketReason": "No Reason given (Ticket opened using emoji)",
					"ticketStatus": "opened"
				}
				tickets_data["tickets"].append(ticket_1)
				counts[str(guild.id)]["ticket_number"] += 1
				counts["id"]["ticket_id"] += 1
				json.dump(counts, open(self.bot.counts_json, "w"), indent='\t')
				json.dump(tickets_data, open(self.bot.tickets_json, 'w'), indent='\t')

	@ticket.command(help="Close a active ticket!")
	async def close(self, ctx: commands.Context, ticket_id: int):
		tickets_data = json.load(open(self.bot.tickets_json))
		transcripts = None
		for ticket in tickets_data['tickets']:
			if ticket_id == int(ticket['ticketID']):
				ticket_owner = ctx.guild.get_member(int(ticket['ticketAuthor'].split(' ')[-1].strip('( )')))
				if ctx.channel.name == f"{str(ctx.author.name).lower()}-{ctx.author.discriminator}" or discord.utils.get(ctx.guild.roles,
				                                                                                                         name="Support") in ctx.author.roles or ctx.author.id == ctx.guild.owner_id:
					try:
						transcripts = reversed(list(await ctx.channel.history().flatten()))
					except discord.errors.NotFound:
						pass
					transcript_temp = f"Transcript for {ticket_owner.name}#{ticket_owner.discriminator} ({ticket_owner.id}) \n"
					file1 = BytesIO(initial_bytes=bytes(transcript_temp + "\n".join(
						f"{transcript.author.name}#{transcript.author.discriminator} ({transcript.author.id}): {transcript.content}" for transcript in transcripts),
					                                    encoding="utf-8"))
					await ticket_owner.send(file=discord.File(file1, filename=f"{ticket_owner.name}_{ticket_owner.discriminator}_{ctx.channel.id}.txt"))
					file1.close()
					await ctx.channel.delete()
					ticket['ticketStatus'] = 'closed'
					ticket['ticketClosedTime'] = get_date_from_short_form_and_unix_time()[1]
		json.dump(tickets_data, open(self.bot.tickets_json, 'w'), indent='\t')

	@ticket.group(name="emoji")
	async def ticket_emoji(self, ctx: commands.Context):
		tickets_data = json.load(open(self.bot.tickets_json))
		if str(ctx.guild.id) not in tickets_data:
			tickets_data[str(ctx.guild.id)] = {}
			tickets_data[str(ctx.guild.id)]['ticket_emoji'] = []
		embed = discord.Embed()
		embed.title = "Available emojis for the ticket in this server!"
		msg = ''
		for index, emoji in enumerate(tickets_data[str(ctx.guild.id)]['ticket_emoji'], start=1):
			msg += f"{index}. {emoji}"
		embed.description = msg
		await ctx.send(embed=embed)
		json.dump(tickets_data, open(self.bot.tickets_json, "w"), indent='\t')

	@ticket_emoji.command(name="set")
	async def set_emoji(self, ctx: commands.Context, emoji_1, index: int):
		tickets_data = json.load(open(self.bot.tickets_json))
		if str(ctx.guild.id) not in tickets_data:
			tickets_data[str(ctx.guild.id)] = {}
			tickets_data[str(ctx.guild.id)]['ticket_emoji'] = []
		tickets_data[str(ctx.guild.id)]['ticket_emoji'].insert(index, emoji_1)
		await ctx.send(f"Set emoji {emoji_1} in index {index}")
		json.dump(tickets_data, open(self.bot.tickets_json, "w"), indent='\t')

	@ticket_emoji.command(name="add")
	async def add_emoji(self, ctx: commands.Context, emoji_1):
		tickets_data = json.load(open(self.bot.tickets_json))
		if str(ctx.guild.id) not in tickets_data:
			tickets_data[str(ctx.guild.id)] = {}
			tickets_data[str(ctx.guild.id)]['ticket_emoji'] = []
		tickets_data[str(ctx.guild.id)]['ticket_emoji'].append(emoji_1)
		await ctx.send(f"Added emoji {emoji_1} to index {len(tickets_data[str(ctx.guild.id)]['ticket_emoji']) - 1}")
		json.dump(tickets_data, open(self.bot.tickets_json, "w"), indent='\t')

	@ticket_emoji.command(name="remove")
	async def remove_emoji(self, ctx: commands.Context, emoji_1):
		tickets_data = json.load(open(self.bot.tickets_json))
		if str(ctx.guild.id) not in tickets_data:
			tickets_data[str(ctx.guild.id)] = {}
			tickets_data[str(ctx.guild.id)]['ticket_emoji'] = []
		index = tickets_data[str(ctx.guild.id)]['ticket_emoji'].remove(emoji_1)
		await ctx.send(f"Removed emoji {emoji_1} to index {index}")
		json.dump(tickets_data, open(self.bot.tickets_json, "w"), indent='\t')


def setup(bot):
	bot.add_cog(Ticket(bot))
