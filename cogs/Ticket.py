from io import BytesIO

import discord
from discord.ext import commands

from cogs.utils.timeformat_bot import get_date_from_short_form_and_unix_time


class Ticket(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		guild: discord.Guild = self.bot.get_guild(payload.guild_id)
		emoji = payload.emoji
		overwrites = {
			guild.default_role: discord.PermissionOverwrite(read_messages=False),
			guild.get_member(payload.user_id): discord.PermissionOverwrite(read_messages=True),
			guild.get_role(703248650129899561): discord.PermissionOverwrite(read_messages=True)
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


def setup(bot):
	bot.add_cog(Ticket(bot))
