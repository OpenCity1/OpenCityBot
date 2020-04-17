__author__ = "Sairam"

import discord
from discord.ext import commands
import random


class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='99!', help='Gives a random brooklyn 99 quote')
	async def _99(self, ctx: discord.ext.commands.context.Context):
		brooklyn_99_quotes = [
			'I\'m the human form of the 💯 emoji.',
			'Bingpot!',
			(
				'Cool. Cool cool cool cool cool cool cool, '
				'no doubt no doubt no doubt no doubt.'
			)
		]
		response = random.choice(brooklyn_99_quotes)
		await ctx.send(response)

	@commands.command(name='8ball', help='Answers your questions ;)')
	async def _8ball(self, ctx: discord.ext.commands.context.Context, *, question):
		replies = [
			"As I see it, yes.",
			"Ask again later.",
			"Better not tell you now.",
			"Cannot predict now.",
			"Concentrate and ask again.",
			"Don’t count on it.",
			"It is certain.",
			"It is decidedly so.",
			"Most likely.",
			"My reply is no.",
			"My sources say no.",
			"Outlook not so good.",
			"Outlook good.",
			"Reply hazy, try again.",
			"Signs point to yes.",
			"Very doubtful.",
			"Without a doubt.",
			"Yes.",
			"Yes – definitely.",
			"You may rely on it."
		]
		await ctx.send(
			f'Question: {question}\n'
			f'Answer: {random.choice(replies)}'
		)

	@commands.command(help="Says what you send.")
	async def say(self, ctx: discord.ext.commands.context.Context, message=None, channel: discord.TextChannel = None):
		await ctx.send("Message sent")
		if channel is None:
			await ctx.send(message)
		else:
			await channel.send(message)


def setup(bot):
	bot.add_cog(Fun(bot))
