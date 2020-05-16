import datetime
import json
from typing import List, Mapping, Optional

import discord
from discord.ext import commands


class MyHelpCommand(commands.HelpCommand):
	def __init__(self, **options):
		super().__init__(**options)

	async def send_command_help(self, command: commands.Command):
		if (not command.hidden) or await self.context.bot.is_owner(self.context.author):
			embed = discord.Embed()
			embed.title = f"{self.context.prefix}{command.name}"
			embed.colour = discord.Colour.dark_green()
			embed.set_author(name=self.context.bot.user.name, icon_url=self.context.bot.user.avatar_url)
			embed.add_field(name="Usage", value=f"`{self.get_command_signature(command)}`")
			embed.add_field(name="Aliases", value=" | ".join([f"`{alias}`" for alias in command.aliases]) if command.aliases else f"`{command.name}`")
			embed.add_field(name="Module", value=f"{str(command.cog.qualified_name)}")
			embed.description = command.help
			await self.context.send(embed=embed)

	async def send_bot_help(self, mapping: Mapping[Optional[commands.Cog], List[commands.Command]]):
		embed = discord.Embed()
		embed.colour = discord.Colour.dark_blue()
		embed.title = f"Need some help, right? Get it here!"
		embed.set_author(name=self.context.bot.user.name, icon_url=self.context.bot.user.avatar_url)
		for cogs in mapping.keys():
			if cogs is not None:
				if len(cogs.get_commands()) != 0:
					embed.add_field(name=cogs.qualified_name, value=", ".join([
						f"`{self.context.prefix}{command}`" for command in cogs.get_commands() if not command.hidden or await self.context.bot.is_owner(self.context.author)]),
					                inline=False)
		await self.context.author.send(embed=embed)

	async def send_cog_help(self, cog: commands.Cog):
		embed = discord.Embed()
		embed.colour = discord.Colour.dark_gold()
		embed.title = cog.qualified_name
		embed.set_author(name=self.context.bot.user.name, icon_url=self.context.bot.user.avatar_url)
		for command in cog.get_commands():
			if command is not None:
				embed.add_field(name=command.name, value=command.help, inline=False)
		await self.context.send(embed=embed)

	async def send_group_help(self, group):
		embed = discord.Embed()
		embed.colour = discord.Colour.dark_orange()
		embed.title = group.qualified_name
		embed.description = f"Usage: `{self.get_command_signature(group)}`\nAliases: {' | '.join([f'`{alias}`' for alias in group.aliases]) if group.aliases else f'`{group.name}`'}"
		embed.set_author(name=self.context.bot.user.name, icon_url=self.context.bot.user.avatar_url)
		for command in group.commands:
			embed.add_field(name=command.name, value=command.help)
		await self.context.send(embed=embed)

	def get_command_signature(self, command):
		return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)


class Information(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self._original_help_command = bot.help_command
		bot.help_command = MyHelpCommand()
		bot.help_command.cog = self

	def cog_unload(self):
		self.bot.help_command = self._original_help_command

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

	@commands.command(help='Pings the bot and gives latency')
	async def ping(self, ctx: discord.ext.commands.context.Context):
		time_before = datetime.datetime.utcnow()
		message = await ctx.send(f'Pong! `{round(self.bot.latency * 1000)}ms\\` latency')
		time_after = datetime.datetime.utcnow() - time_before
		await message.edit(content=f"Pong! `{round(self.bot.latency * 1000)}ms\\{round(time_after.total_seconds() * 100)}ms` Latency")

	@commands.command(help="Gives you invite for this bot!")
	async def invite(self, ctx: commands.Context):
		embed = discord.Embed(
			title="Invite Me!",
			color=discord.Colour.gold(),
			description=("This is my invite link. You can use this link to add me to your server!\n"
			             f"Link can be found [here]({self.bot.invite_url})."
			             )
		)
		await ctx.send(embed=embed)

	@commands.command(help="Gives you the bot's uptime!")
	async def uptime(self, ctx: commands.Context):
		delta_uptime = datetime.datetime.utcnow() - self.bot.start_time
		hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
		minutes, seconds = divmod(remainder, 60)
		days, hours = divmod(hours, 24)
		await ctx.send(f"Uptime: {days}d, {hours}h, {minutes}m, {seconds}s")


def setup(bot):
	bot.add_cog(Information(bot))
