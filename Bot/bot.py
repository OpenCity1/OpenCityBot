# import Bot.leveling as leveling
import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))

bot = commands.Bot(command_prefix='!')

roles_needed = ["Muted Members", "Banned Members", "Kicked Members"]


@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name="OpenCity \nType !help to get started"))
	# guild = discord.utils.get(client.guildTry .helps, id=GUILD_ID)
	for guild_index, guild in enumerate(bot.guilds):
		print(
			f'{bot.user} is connected to the following guild:\n'
			f'{guild.name}(id: {guild.id})'
		)

		members = '\n - '.join([member.name for member in guild.members])
		print(f'Guild Members of {guild.name} are:\n - {members}')
		if guild_index != (len(bot.guilds) - 1):
			print('\n\n\n', end="")

		role_names = [role.name for role in guild.roles]

		for role in roles_needed:
			if role not in role_names:
				await guild.create_role(name=role)

#
# @bot.event
# async def on_member_join(member):
# 	guild = discord.utils.get(bot.guilds, id=GUILD_ID)
# 	await member.create_dm()
# 	await member.dm_channel.send(welcome_message.format(guild.name))
#
#
# async def run_when_dm_response(message):
# 	if int(message.content) in response_dict.keys():
# 		try:
# 			await message.channel.send(response_dict[int(message.content)])
# 		except ValueError:
# 			await message.channel.send("You send a wrong message")
# 	else:
# 		await message.channel.send(f"Sorry we just have {len(response_dict.keys())} questions as FAQ. More will be added.")
#
#
# @bot.event
# async def on_message(message):
# 	if message.author == bot.user:
# 		return
#
# 	if message.channel.type == discord.ChannelType.private:
# 		await run_when_dm_response(message)
#
# 	# await leveling.levelling(message)
#
# 	await bot.process_commands(message)
#
#
# @bot.event
# async def on_member_update(before, after):
# 	# await leveling.level_update(before, after)
# 	pass

#
# @bot.command(help='Pings the bot and gives latency')
# async def ping(ctx: discord.ext.commands.context.Context):
# 	await ctx.send(f'Pong! {round(bot.latency * 1000)}ms Latency')
#
#
# @bot.command()
# async def load(ctx, extension):
# 	bot.load_extension(f'cogs.{extension}')
# 	await ctx.send(f"Loaded {extension}")
#
#
# @bot.command()
# async def unload(ctx, extension):
# 	bot.unload_extension(f'cogs.{extension}')
# 	await ctx.send(f"Unloaded {extension}")
#
#
# @bot.command()
# async def reload(ctx, extension):
# 	bot.unload_extension(f'cogs.{extension}')
# 	bot.load_extension(f'cogs.{extension}')
# 	await ctx.send(f"Reloaded {extension}")


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)
