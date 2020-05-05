from io import BytesIO
from typing import List

import discord
from discord.ext import commands

from cogs.utils.timeformat_bot import get_date_from_short_form_and_unix_time


class Ticket(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.ticket_owner_list: List[discord.Member] = []

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		guild: discord.Guild = self.bot.get_guild(payload.guild_id)
		if not discord.utils.find(lambda r: r.name == "Support", guild.roles):
			await guild.create_role(name="Support", color=discord.Colour(0x80068b), hoist=True, mentionable=True)
		emoji = payload.emoji
		overwrites = {
			guild.default_role: discord.PermissionOverwrite(read_messages=False),
			guild.get_member(payload.user_id): discord.PermissionOverwrite(read_messages=True),
			discord.utils.find(lambda r: r.name == "Support", guild.roles): discord.PermissionOverwrite(read_messages=True)
		}
		user: discord.Member = guild.get_member(payload.user_id)
		embed = discord.Embed(
			title=f"Thank you for creating a ticket! {user.name}",
			description=f"Thank you for creating a ticket! {user.mention}\nWe'll get back to you as soon as possible.",
		)
		embed.set_footer(text=f"{guild.name} | {get_date_from_short_form_and_unix_time()[1]}")
		if str(emoji) == "\U0001f44d":
			if discord.utils.get(guild.categories, name="Support") not in guild.categories:
				await guild.create_category(name="Support")
			channel = await guild.create_text_channel(name=f'{user.name}-{user.discriminator}', category=discord.utils.get(user.guild.categories, name="Support"),
			                                          overwrites=overwrites)
			await channel.edit(topic=f"Opened by {user.name} - All messages sent to this channel are being recorded.")
			await channel.send(embed=embed)
			self.ticket_owner_list.append(user)

	@commands.command(help="Close a active ticket!")
	async def close(self, ctx: commands.Context):
		transcripts = None
		if ctx.channel.name == f"{str(ctx.author.name).lower()}-{ctx.author.discriminator}" or discord.utils.get(ctx.guild.roles,
		                                                                                                         name="Support") in ctx.author.roles or ctx.author.id == ctx.guild.owner_id:
			for ticket_owner in self.ticket_owner_list:
				if ctx.channel.name == f"{str(ticket_owner.name).lower()}-{ticket_owner.discriminator}":
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


def setup(bot):
	bot.add_cog(Ticket(bot))
