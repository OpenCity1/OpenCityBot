import datetime
import json
import os
from typing import List, Mapping, Optional

import discord
from discord.ext import commands


class MyHelpCommand(commands.HelpCommand):
	async def send_command_help(self, command: commands.Command):
		embed = discord.Embed()
		embed.title = f"{self.context.bot.command_prefix(self.context.bot, self.context.message)}{command.name}"
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
					embed.add_field(name=cogs.qualified_name, value=" , ".join(f"`{command}`" for command in cogs.get_commands()), inline=False)
		await self.context.send(embed=embed)

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
		embed.set_author(name=self.context.bot.user.name, icon_url=self.context.bot.user.avatar_url)
		for command in group.commands:
			embed.add_field(name=command.name, value=command.help)
		await self.context.send(embed=embed)

	def get_command_signature(self, command):
		return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)


class System(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self._original_help_command = bot.help_command
		bot.help_command = MyHelpCommand()
		bot.help_command.cog = self

	def cog_unload(self):
		self.bot.help_command = self._original_help_command

	@commands.command(help='Pings the bot and gives latency')
	async def ping(self, ctx: discord.ext.commands.context.Context):
		time_before = datetime.datetime.utcnow()
		message = await ctx.send(f'Pong! `{round(self.bot.latency * 1000)}ms\\` latency')
		time_after = datetime.datetime.utcnow() - time_before
		await message.edit(content=f"Pong! `{round(self.bot.latency * 1000)}ms\\{round(time_after.total_seconds() * 100)}ms` Latency")

	@commands.command(help="Loads an extension")
	@commands.is_owner()
	async def load(self, ctx, extension):
		os.chdir("..")
		self.bot.load_extension(f'cogs.{extension}')
		await ctx.send(f"Loaded {extension}")

	@commands.command(help="Unloads an extension")
	@commands.is_owner()
	async def unload(self, ctx, extension):
		os.chdir("..")
		self.bot.unload_extension(f'cogs.{extension}')
		await ctx.send(f"Unloaded {extension}")

	@commands.command(help="Reloads an extension")
	@commands.is_owner()
	async def reload(self, ctx, extension):
		os.chdir("..")
		self.bot.unload_extension(f'cogs.{extension}')
		self.bot.load_extension(f'cogs.{extension}')
		await ctx.send(f"Reloaded {extension}")

<<<<<<< HEAD
=======
	@commands.command(help="Gives you invite for this bot!")
	async def invite(self, ctx: commands.Context):
		embed = discord.Embed(
			title="Invite Me!",
			color=discord.Colour.gold(),
			description=("This is my invite link. You can use this link to add me to your server!\n"
			             "Link can be found [here](https://discordapp.com/api/oauth2/authorize?client_id=693401671836893235&permissions=8&scope=bot)."
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

	@commands.command(name="setprefix", help="Sets the prefix for a guild!")
	async def set_prefix(self, ctx: commands.Context, prefix):
		prefix_list = json.load(open(os.path.dirname(os.path.dirname(__file__)) + "\prefix.json", "r"))
		prefix_list[str(ctx.guild.id)]["prefix"] = prefix
		with open(os.path.dirname(os.path.dirname(__file__)) + "\prefix.json", "w") as file:
			json.dump(prefix_list, file, indent=4)
		await ctx.send(f"Set prefix to {prefix}")

>>>>>>> 4debb5edfb20bf97d01cc51d7e12f210a5953779

def setup(bot):
	bot.add_cog(System(bot))
