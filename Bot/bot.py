import os
import random

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))

client = discord.Client()

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


@client.event
async def on_ready():
	guild = discord.utils.get(client.guilds, id=GUILD_ID)
	print(
		f'{client.user} is connected to the following guild:\n'
		f'{guild.name}(id: {guild.id})'
	)

	members = '\n - '.join([member.name for member in guild.members])
	print(f'Guild Members:\n - {members}')


@client.event
async def on_member_join(member):
	guild = discord.utils.get(client.guilds, id=GUILD_ID)
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


@client.event
async def on_message(message):
	if message.author == client.user:
		return
	brooklyn_99_quotes = [
		'I\'m the human form of the 💯 emoji.',
		'Bingpot!',
		(
			'Cool. Cool cool cool cool cool cool cool, '
			'no doubt no doubt no doubt no doubt.'
		)
	]
	if message.content == '99!':
		response = random.choice(brooklyn_99_quotes)
		await message.channel.send(response)

	if message.channel.type == discord.ChannelType.private:
		await run_when_dm_response(message)
	# if message.channel.type == discord.ChannelType.private:
	# 	if int(message.content) in response_dict.keys():
	# 		try:
	# 			await message.channel.send(response_dict[int(message.content)])
	# 		except ValueError:
	# 			await message.channel.send("You send a wrong message")
	# 	else:
	# 		await message.channel.send("Sorry we just have 5 questions. More will be added.")



client.run(TOKEN)
