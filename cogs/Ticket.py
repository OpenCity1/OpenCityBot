import json
from io import BytesIO

import discord
from discord.ext import commands

from cogs.utils.timeformat_bot import get_date_from_short_form_and_unix_time


class Ticket(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def cog_check(self, ctx):
		guild_data = json.load(open(self.bot.guilds_json))
		enabled = guild_data[str(ctx.guild.id)]["enabled"]
		if f"cogs.{ctx.cog.qualified_name}" in enabled:
			return True
		return False

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		guild: discord.Guild = self.bot.get_guild(payload.guild_id)
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
			title=f"Thank you for creating a ticket! {user.name}",
			description=f"Thank you for creating a ticket! {user.mention}\nWe'll get back to you as soon as possible.",
		)
		embed.set_footer(text=f"{guild.name} | {get_date_from_short_form_and_unix_time()[1]}")
		if str(emoji) == "👎":
			if discord.utils.get(guild.categories, name="Support") not in guild.categories:
				await guild.create_category(name="Support")
			channel = await guild.create_text_channel(name=f'{user.name}-{user.discriminator}', category=discord.utils.get(user.guild.categories, name="Support"),
			                                          overwrites=overwrites)
			await channel.edit(topic=f"Opened by {user.name} - All messages sent to this channel are being recorded.")
			await channel.send(embed=embed)

	@commands.command(help="Close a active ticket!")
	async def close(self, ctx: commands.Context):
		if ctx.channel.name == f"{str(ctx.author.name).lower()}-{ctx.author.discriminator}" or discord.utils.get(ctx.guild.roles,
		                                                                                                         name="Support") in ctx.author.roles or ctx.author.id == ctx.guild.owner_id:
			transcripts = await ctx.channel.history().flatten()
			with BytesIO() as file1:
				for transcript in transcripts:
					print((str(transcript.content)))
					file1.write((str(transcript.content).encode()) + '\n'.encode())
					x = file1.readline(1)
					print(x)
				await ctx.author.send(file=discord.File(file1, filename=f"{ctx.author.name}_{ctx.author.discriminator}_{ctx.channel.id}.txt"))
			await ctx.channel.delete()

	@commands.command()
	async def set_emoji(self, ctx: commands.Context, emoji: discord.Emoji):
		tickets_data = json.load(open(self.bot.tickets_json))


def setup(bot):
	bot.add_cog(Ticket(bot))
