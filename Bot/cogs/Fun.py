__author__ = "Sairam"

import json
import random
from typing import Optional

import discord
import wikipedia
from discord.ext import commands


class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def cog_check(self, ctx):
		if ctx.channel.type == discord.ChannelType.private:
			return True
		if await self.bot.is_owner(ctx.author):
			return True
		guild_data = json.load(open(self.bot.guilds_json))
		enabled = guild_data[str(ctx.guild.id)]["enabled"]
		if f"Bot.cogs.{self.qualified_name}" in enabled:
			return True
		return False

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

	@commands.command(name="wikipedia", help="Gives you the page in wikipedia", hidden=True)
	async def wikipedia(self, ctx, search):
		result = wikipedia.search(search, results=1)
		page = wikipedia.page(result)
		await ctx.send(page)

	@commands.command(name="urban (WIP or Not Implemented)", help="Give you the page from urban dictionary", hidden=True)
	async def urban(self, search):
		pass

	@commands.command(help="Says what you sent using tts!")
	async def echo(self, ctx, channel: Optional[discord.TextChannel] = None, *, message=None):
		if message is not None:
			if channel is None:
				await ctx.send(message, tts=True)
			else:
				await channel.send(message, tts=True)
				await ctx.send("Message sent")
		else:
			await ctx.send(f"Message is not filled. Please send the message to be sent. {ctx.author.mention}")

	@commands.group(name="convert_to", help="Converts a given string into a subcommand formatted string")
	async def _convert_to(self, ctx: commands.Context):
		pass

	@_convert_to.command(help="Gives you up-side down text!")
	async def up_down(self, ctx, *, string: str):
		input_table = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~!@#$%^&*()_+{}|:\"<>?[]\\;',./"
		output_table = "".join(reversed(list("/˙',؛\[]¿<>„:|{}+‾()*&^%$#@¡~0987654321ZʎXMΛ∩⊥SᴚὉԀONW˥ʞſIHƃℲƎᗡϽq∀zʎxʍʌnʇsɹbdouɯןʞɾıɥƃɟǝpɔqɐ")))
		translation = string.maketrans(input_table, output_table)

		output_string = string.translate(translation)
		output_reverse = "".join(reversed(list(output_string)))
		await ctx.send(output_reverse)

	@_convert_to.command(help="Gives you the reversed string!")
	async def reverse(self, ctx, *, string: str):
		output_reverse = "".join(reversed(list(string)))
		await ctx.send(output_reverse)

	@_convert_to.command(help="Gives you a formatted Small-Caps")
	async def small_caps(self, ctx, *, string):
		input_table = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~!@#$%^&*()_+{}|:\"<>?[]\;',./"
		output_table = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~!@#$%^&*()_+{}|:\"<>?[]\;',./"

		translation = string.maketrans(input_table, output_table)

		output_string = string.translate(translation)
		await ctx.send(output_string)

	@_convert_to.command(help="Gives you a vapour-waved string")
	async def vapour_wave(self, ctx, *, string):
		input_table = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~!@#$%^&*()_+{}|:\"<>?[]\;',./"
		output_table = "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ１２３４５６７８９０～！＠＃＄％＾＆＊（）＿＋｛｝｜：＂＜＞？［］＼；＇，．／"

		translation = string.maketrans(input_table, output_table)

		output_string = string.translate(translation)
		await ctx.send(output_string)

	@_convert_to.command(help="Gives you a monospaced string")
	async def monospace(self, ctx, *, string):
		input_table = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~!@#$%^&*()_+{}|:\"<>?[]\;',./"
		output_table = "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿0~!@#$%^&*()_+{}|:\"<>?[]\;',./"

		translation = string.maketrans(input_table, output_table)

		output_string = string.translate(translation)
		await ctx.send(output_string)

	@_convert_to.command(help="Gives you a formatted string with cursive!")
	async def cursive_script(self, ctx, *, string):
		input_table = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~!@#$%^&*()_+{}|:\"<>?[]\;',./"
		output_table = "𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵1234567890~!@#$%^&*()_+{}|:\"<>?[]\;',./"

		translation = string.maketrans(input_table, output_table)

		output_string = string.translate(translation)
		await ctx.send(output_string)

	@_convert_to.command(help="Gives you a currency styled a format!")
	async def currency_styled_text(self, ctx, *, string):
		input_table = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~!@#$%^&*()_+{}|:\"<>?[]\;',./"
		output_table = "₳฿₵ĐɆ₣₲ⱧłJ₭Ⱡ₥₦Ø₱QⱤ₴₮ɄV₩ӾɎⱫ₳฿₵ĐɆ₣₲ⱧłJ₭Ⱡ₥₦Ø₱QⱤ₴₮ɄV₩ӾɎⱫ1234567890~!@#$%^&*()_+{}|:\"<>?[]\;',./"

		translation = string.maketrans(input_table, output_table)

		output_string = string.translate(translation)
		await ctx.send(output_string)

	@_convert_to.command(help="Gives you a formatted old_english_styled string!")
	async def old_english_style(self, ctx, *, string):
		input_table = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~!@#$%^&*()_+{}|:\"<>?[]\;',./"
		output_table = "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ1234567890~!@#$%^&*()_+{}|:\"<>?[]\;',./"

		translation = string.maketrans(input_table, output_table)

		output_string = string.translate(translation)
		await ctx.send(output_string)


def setup(bot):
	bot.add_cog(Fun(bot))
