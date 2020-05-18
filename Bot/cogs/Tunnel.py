import json
from io import BytesIO

import discord
from discord.ext import commands

from Bot.cogs.utils.timeformat_bot import indian_standard_time_now


class Tunnel(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	def cog_check(self, ctx):
		if ctx.channel.type == discord.ChannelType.private:
			return True
		guild_data = json.load(open(self.bot.guilds_json))
		enabled = guild_data[str(ctx.guild.id)]["enabled"]
		if f"Bot.cogs.{self.qualified_name}" in enabled:
			return True
		return False

	@commands.group()
	async def tunnel(self, ctx: commands.Context):
		pass

	@tunnel.command(name="new")
	async def tunnel_new(self, ctx: commands.Context, user: discord.Member, reason: str):
		counts = json.load(open(self.bot.counts_json))
		if "id" not in counts.keys():
			counts["id"] = {}
		if str(ctx.guild.id) not in counts.keys():
			counts[str(ctx.guild.id)] = {}
		if "tunnel_id" not in counts["id"].keys():
			counts["id"]["tunnel_id"] = self.bot.start_number
		if "tunnel_number" not in counts[str(ctx.guild.id)].keys():
			counts[str(ctx.guild.id)]["tunnel_number"] = 1
		overwrites = {
			ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
			ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True),
			user: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True)
		}
		embed = discord.Embed(
			title=f"Thank you for creating a tunnel! {ctx.author.name} This is Tunnel #{counts[str(ctx.guild.id)]['tunnel_number']}",
			description=f"Thank you for creating a tunnel! {ctx.author.mention}\nWe'll get back to you as soon as possible.",
		)
		embed.set_footer(text=f"TunnelID: {counts['id']['tunnel_id']} | {indian_standard_time_now()[1]}")
		if discord.utils.get(ctx.guild.categories, name="Tunnels") not in ctx.guild.categories:
			await ctx.guild.create_category(name="Tunnels")
		channel = await ctx.guild.create_text_channel(name=f'{ctx.author.name}-{ctx.author.discriminator}-----{user.name}-{user.discriminator}',
		                                              category=discord.utils.get(ctx.guild.categories, name="Tunnels"),
		                                              overwrites=overwrites)
		await channel.edit(topic=f"Opened by {ctx.author.name} - All messages sent to this channel are being recorded.")
		await channel.send(embed=embed)

		tunnels_data = json.load(open(self.bot.tunnels_json))
		if "tunnels" not in tunnels_data.keys():
			tunnels_data["tunnels"] = []

		tunnel_1 = {
			"tunnelID": counts['id']["tunnel_id"],
			"tunnelAuthor": f"{str(ctx.author.name).replace(' ', '-')}#{ctx.author.discriminator} ({ctx.author.id})",
			"tunnelOpenedTime": indian_standard_time_now()[1],
			"tunnelClosedTime": "Not closed till now!",
			"tunnelGuildID": f"{ctx.guild.id}",
			"tunnelReason": f"{reason}",
			"tunnelUser": f"{str(user.name).replace(' ', '-')}#{user.discriminator} ({user.id})",
			"tunnelStatus": "opened"
		}
		tunnels_data["tunnels"].append(tunnel_1)
		counts[str(ctx.guild.id)]["tunnel_number"] += 1
		counts["id"]["tunnel_id"] += 1
		json.dump(counts, open(self.bot.counts_json, "w"), indent='\t')
		json.dump(tunnels_data, open(self.bot.tunnels_json, 'w'), indent='\t')

	@tunnel.command(name="close")
	async def tunnel_close(self, ctx: commands.Context, tunnel_id):
		tunnels_data = json.load(open(self.bot.tunnels_json))
		transcripts = None
		for tunnel in tunnels_data['tunnels']:
			if tunnel_id == int(tunnel['tunnelID']):
				tunnel_owner = ctx.guild.get_member(int(tunnel['tunnelAuthor'].split(' ')[-1].strip('( )')))
				if ctx.channel.name == f"{str(ctx.author.name).lower()}-{ctx.author.discriminator}" or discord.utils.get(ctx.guild.roles,
				                                                                                                         name="Support") in ctx.author.roles or ctx.author.id == ctx.guild.owner_id:
					try:
						transcripts = reversed(list(await ctx.channel.history().flatten()))
					except discord.errors.NotFound:
						pass
					transcript_temp = f"Transcript for {tunnel_owner.name}#{tunnel_owner.discriminator} ({tunnel_owner.id}) \n"
					file1 = BytesIO(initial_bytes=bytes(transcript_temp + "\n".join(
						f"{transcript.author.name}#{transcript.author.discriminator} ({transcript.author.id}): {transcript.content}" for transcript in transcripts),
					                                    encoding="utf-8"))
					await tunnel_owner.send(file=discord.File(file1, filename=f"{tunnel_owner.name}_{tunnel_owner.discriminator}_{ctx.channel.id}.txt"))
					file1.close()
					await ctx.channel.delete()
					tunnel['tunnelStatus'] = 'closed'
					tunnel['tunnelClosedTime'] = indian_standard_time_now()[1]
		json.dump(tunnels_data, open(self.bot.tunnels_json, 'w'), indent='\t')


def setup(bot):
	bot.add_cog(Tunnel(bot))
