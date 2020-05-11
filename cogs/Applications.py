import asyncio
import json
from typing import Optional

import discord
from discord.ext import commands


class Applications(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	def cog_check(self, ctx):
		if ctx.channel.type == discord.ChannelType.private:
			return True
		if await self.bot.is_owner(ctx.author):
			return True
		guild_data = json.load(open(self.bot.guilds_json))
		enabled = guild_data[str(ctx.guild.id)]["enabled"]
		if f"cogs.{ctx.cog.qualified_name}" in enabled:
			return True
		return False

	@commands.group(aliases=['app', 'a'], invoke_without_command=True, help="Lists all applications")
	async def applications(self, ctx: commands.Context):
		application_data = json.load(open(self.bot.applications_json))
		if str(ctx.guild.id) not in application_data.keys():
			application_data[str(ctx.guild.id)] = {}
		embed = discord.Embed()
		embed.title = "Available applications for this server!"
		msg = ''
		for index, key in enumerate(application_data[str(ctx.guild.id)].keys(), start=1):
			msg += f"{index}. {key}"
		embed.description = msg
		embed.set_author(name=ctx.me.name, icon_url=ctx.me.avatar_url)
		await ctx.send(embed=embed)
		json.dump(application_data, open(self.bot.applications_json, "w"), indent='\t')

	@applications.command(help="Applies a applications")
	async def apply(self, ctx, application_type):
		application_data = json.load(open(self.bot.applications_json))
		if str(ctx.guild.id) not in application_data.keys():
			application_data[str(ctx.guild.id)] = {}
		if application_type not in application_data[str(ctx.guild.id)].keys():
			await ctx.send("The application name you sent is not available in this server!")
			return
		list_of_questions = application_data[str(ctx.guild.id)][application_type]

		await ctx.author.send(f'You\'ve applied for {application_type} application!')
		await ctx.author.send('This is the first question!')

		def check(message: discord.Message) -> bool:
			return message.author == ctx.author

		list_of_answers = []
		for index, question in enumerate(list_of_questions, start=1):
			await ctx.author.send(f"{index}. {str(question).capitalize()}")
			try:
				response_by_user = await self.bot.wait_for('message', check=check, timeout=60)
			except asyncio.TimeoutError:
				await ctx.send(f"You took to long to respond {ctx.author.mention}")
				break
			else:
				if response_by_user in ['close', 'exit']:
					await ctx.author.send("Okay, exiting!")
					break
				list_of_answers.append(response_by_user)
		await ctx.author.send('You\'ve successfully answered all of my questions')
		await ctx.author.send('Thank you for your time!')
		embed = discord.Embed()
		embed.title = f"{ctx.author.name}#{ctx.author.discriminator}"
		for index, (question, answer) in enumerate(zip(list_of_questions, list_of_answers), start=1):
			embed.add_field(name=f"{index}. {question}", value=f"{answer.content}", inline=False)
		await ctx.send(embed=embed)

	@applications.group(invoke_without_command=True, help="Lists all questions of a application.")
	async def questions(self, ctx, application_type):
		application_data = json.load(open(self.bot.applications_json))
		if str(ctx.guild.id) not in application_data.keys():
			application_data[str(ctx.guild.id)] = {}
		if application_type not in application_data[str(ctx.guild.id)].keys():
			await ctx.send("The application name you sent is not available in this server!")
			return
		embed = discord.Embed()
		embed.title = "Available questions for this application on this server!"
		msg = ''
		for index, key in enumerate(application_data[str(ctx.guild.id)][application_type], start=1):
			msg += f"{index}. {key}"
		embed.description = msg
		embed.set_author(name=ctx.me.name, icon_url=ctx.me.avatar_url)
		await ctx.send(embed=embed)
		json.dump(application_data, open(self.bot.applications_json, "w"), indent='\t')

	@questions.command(name="add", help="Adds a question to a application")
	async def question_add(self, ctx, application_type, question, index: Optional[int] = -1):
		application_data = json.load(open(self.bot.applications_json))
		if str(ctx.guild.id) not in application_data.keys():
			application_data[str(ctx.guild.id)] = {}
		if application_type not in application_data[str(ctx.guild.id)].keys():
			await ctx.send("The application name you sent is not available in this server!")
			return
		index_value_if_index_is_minus_one = 0
		if index == -1:
			application_data[str(ctx.guild.id)][application_type].append(question)
			index_value_if_index_is_minus_one = application_data[str(ctx.guild.id)][application_type].index(question)
		elif 0 <= index < len(application_data[str(ctx.guild.id)][application_type]):
			application_data[str(ctx.guild.id)][application_type].insert(index, question)
		else:
			await ctx.send("Index invalid!")
			return
		await ctx.send(f"Added your question at {index if index != -1 else index_value_if_index_is_minus_one}")
		json.dump(application_data, open(self.bot.applications_json, "w"), indent='\t')

	@questions.command(name="remove", help="Removes a question from a application")
	async def question_remove(self, ctx, application_type, question, index: Optional[int] = -1):
		application_data = json.load(open(self.bot.applications_json))
		if str(ctx.guild.id) not in application_data.keys():
			application_data[str(ctx.guild.id)] = {}
		if application_type not in application_data[str(ctx.guild.id)].keys():
			await ctx.send("The application name you sent is not available in this server!")
			return
		index_value_if_index_is_minus_one = 0
		if index == -1:
			index_value_if_index_is_minus_one = application_data[str(ctx.guild.id)][application_type].index(question)
			application_data[str(ctx.guild.id)][application_type].remove(question)
		elif 0 <= index < len(application_data[str(ctx.guild.id)][application_type]):
			application_data[str(ctx.guild.id)][application_type].pop(index)
		else:
			await ctx.send("Index invalid!")
			return
		await ctx.send(f"Removed your question at {index if index != -1 else index_value_if_index_is_minus_one}")
		json.dump(application_data, open(self.bot.applications_json, "w"), indent='\t')

	@applications.command(name='add', help='Adds a application to a server.')
	async def application_add(self, ctx, application_type):
		application_data = json.load(open(self.bot.applications_json))
		if str(ctx.guild.id) not in application_data.keys():
			application_data[str(ctx.guild.id)] = {}
		application_data[str(ctx.guild.id)][application_type] = []
		await ctx.send("application added")
		await ctx.send("please say the amount of question you would like to enter?")

		def int_check(message: discord.Message) -> bool:
			return message.author == ctx.author and type(message.content) == int

		def question_check(message: discord.Message) -> bool:
			return message.author == ctx.author and message.content.endswith('?')

		count = self.bot.wait_for('message', check=int_check)
		for i in range(count):
			question = self.bot.wait_for('message', check=question_check)
			application_data[str(ctx.guild.id)][application_type].append(question)

		await ctx.send("Questions added successfully")
		await ctx.send("To add extra questions or remove unnecessary questions, use `!a questions add {question}`")

	@applications.command(name='remove', help="Removes a application from a server.")
	async def application_remove(self, ctx, application_type):
		application_data = json.load(open(self.bot.applications_json))
		if str(ctx.guild.id) not in application_data.keys():
			application_data[str(ctx.guild.id)] = {}
		application_data[str(ctx.guild.id)].pop(application_type)
		await ctx.send("removed application successfully")


def setup(bot):
	bot.add_cog(Applications(bot))
