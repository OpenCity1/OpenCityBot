import os
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

	def cog_check(self, ctx):
		return self.bot.is_owner(ctx.author)

	def cog_unload(self):
		self.bot.help_command = self._original_help_command

	@commands.command(help="Loads an extension", hidden=True)
	async def load(self, ctx, extension):
		os.chdir("..")
		self.bot.load_extension(f'cogs.{extension}')
		await ctx.send(f"Loaded {extension}")

	@commands.command(help="Unloads an extension", hidden=True)
	async def unload(self, ctx, extension):
		os.chdir("..")
		self.bot.unload_extension(f'cogs.{extension}')
		await ctx.send(f"Unloaded {extension}")

	@commands.command(help="Reloads an extension", hidden=True)
	async def reload(self, ctx, extension):
		os.chdir("..")
		self.bot.unload_extension(f'cogs.{extension}')
		self.bot.load_extension(f'cogs.{extension}')
		await ctx.send(f"Reloaded {extension}")

	@commands.command(hidden=True)
	async def leave_server(self, ctx: commands.Context):
		await ctx.guild.leave()


def setup(bot):
	bot.add_cog(System(bot))
