__author__ = "Sairam"

import random
from typing import Optional

import discord
from discord.ext import commands


class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='99!', help='Gives a random brooklyn 99 quote!')
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

	@commands.command(name='8ball', help='Answers your questions! ;)')
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

	@commands.command(help="Says what you send!")
	async def say(self, ctx: commands.context.Context, channel: Optional[discord.TextChannel] = None, *, message=None):
		if message is not None:
			if channel is None:
				await ctx.send(message)
			else:
				await channel.send(message)
				await ctx.send("Message sent")
		else:
			await ctx.send(f"Message is not filled. Please send the message to be sent. {ctx.author.mention}")

	# @say.error
	# async def error_say(self, ctx, error):
	# 	if isinstance(error, discord.HTTPException):
	# 		await ctx.send(f"Message is not filled. Please send the message to be sent. {ctx.author.mention}")

	@commands.command(name='spaceit!', help="Add a space between each letter!")
	async def space_it(self, ctx: commands.Context, *, message: str):
		await ctx.send(" ".join(message))

	@commands.command(name='randomizecase', help="Randomizes each letter into capital or small", aliases=['randomcase', 'caserandom'])
	async def randomize_case(self, ctx: commands.Context, *, message: str):
		await ctx.send("".join(random.choice((str1.upper(), str1.lower())) for str1 in message))

	@commands.command(name='flipthecoin!', help="Flips the coin!", aliases=['flip', 'coinflip'])
	async def flip_the_coin(self, ctx: commands.Context):
		await ctx.send(f"You got {str(random.choice(('Head', 'Tail'))).lower()}")

	@commands.command(name='voter!', help='Helps you to decide anything!', aliases=['vote', 'voteforme'])
	async def voter(self, ctx: commands.Context, *, messages: str):
		await ctx.send(
			f"Answer: {random.choice(messages.split(','))}"
		)

	@commands.command(name="wikipedia (WIP or Not Implemented)", help="Gives you the page in wikipedia")
	async def wikipedia(self, search):
		pass

	@commands.command(name="urban (WIP or Not Implemented)", help="Give you the page from urban dictionary")
	async def urban(self, search):
		pass


def setup(bot):
	bot.add_cog(Fun(bot))
