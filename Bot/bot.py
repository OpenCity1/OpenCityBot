import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))

bot = commands.Bot(command_prefix='.')

welcome_message = 'Hello, welcome to the {} Discord-server! \n \n I can answer most of your questions.\n Most of the question can be answered by reading faq though!! 😀 \n You can ask me if you want: \n \
\n \
1: What is this? or what is the server meant for?\n \
2: Who is the administrator? or owner?\n \
3: When will OpenCity be released?\n \
4: How far are the game has progressed so far?\n \
5: Who made this bot?\n\n \
To ask me just type in the number in front of the question!'

response_dict = {1: 'This is the support discord for the OpenCity city building game.', 2: 'Sairam', 3: 'Please check the faq', 4: 'We have made Main Menu and some icons',
                 5: 'NameKhan72, Sairam, Wizard BINAY'}


@bot.event
async def on_ready():
	# guild = discord.utils.get(client.guilds, id=GUILD_ID)
	for guild_index, guild in enumerate(bot.guilds):
		print(
			f'{bot.user} is connected to the following guild:\n'
			f'{guild.name}(id: {guild.id})'
		)

		members = '\n - '.join([member.name for member in guild.members])
		print(f'Guild Members of {guild.name} are:\n - {members}')
		if guild_index != (len(bot.guilds) - 1):
			print('\n\n\n', end="")


@bot.event
async def on_member_join(member):
	guild = discord.utils.get(bot.guilds, id=GUILD_ID)
	await member.create_dm()
	await member.dm_channel.send(welcome_message.format(guild.name))


async def run_when_dm_response(message):
	if int(message.content) in response_dict.keys():
		try:
			await message.channel.send(response_dict[int(message.content)])
		except ValueError:
			await message.channel.send("You send a wrong message")
	else:
		await message.channel.send(f"Sorry we just have {len(response_dict.keys())} questions as FAQ. More will be added.")


@bot.event
async def on_message(message):
	if message.author == bot.user:
		return

	if message.channel.type == discord.ChannelType.private:
		await run_when_dm_response(message)

	await bot.process_commands(message)


@bot.command(name='99!', help='Gives a random brooklyn 99 quote')
async def _99(ctx: discord.ext.commands.context.Context):
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


@bot.command(help='Pings the bot and gives latency')
async def ping(ctx: discord.ext.commands.context.Context):
	await ctx.send(f'Pong! {round(bot.latency * 1000)}ms Latency')


@bot.command(help='Bans the given user')
async def ban(ctx: discord.ext.commands.context.Context, member: discord.Member, *, reason="No reason provided"):
	await member.ban(reason=reason)
	await ctx.send(f'{member} is banned because of {reason}.')


@bot.command(help='Kicks the given user')
async def kick(ctx: discord.ext.commands.context.Context, member: discord.Member, *, reason="No reason provided"):
	await member.kick(reason=reason)
	await ctx.send(f'{member} is kicked because of {reason}.')


@bot.command(help='Unbans the given user')
async def unban(ctx: discord.ext.commands.context.Context, member: str):
	ban_entries = await ctx.guild.bans()
	member_name, member_discriminator = member.split("#")

	for ban_entry in ban_entries:
		user = ban_entry.user
		if (user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
	await ctx.send(f'{member} is unbanned.')


@bot.command(name='8ball', help='Answers your questions ;)')
async def _8ball(ctx: discord.ext.commands.context.Context, *, question):
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


@bot.command(help="Says what you send.")
async def say(ctx: discord.ext.commands.context.Context, message):
	await ctx.send(message)


@bot.command(help="Purges the given amount of messages")
async def purge(ctx: discord.ext.commands.context.Context, amount_of_messages=0):
	await ctx.channel.purge(limit=amount_of_messages)


bot.run(TOKEN)
