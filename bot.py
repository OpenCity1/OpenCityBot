import datetime
import json
import logging
import os
import random

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DEFAULT_PREFIX')
USERS_FILE = os.getenv('USERS_FILE')
PREFIX_FILE = os.getenv('PREFIX_JSON')


def get_prefix(bot, message):
	try:
		prefix_list = json.load(open("prefix.json", "r"))
	except (json.JSONDecodeError, FileNotFoundError):
		prefix_list = {}
	try:
		if str(message.guild.id) not in prefix_list.keys():
			prefix_list[str(message.guild.id)] = {"prefix": list(PREFIX.split(" "))}
	except AttributeError:
		pass
	with open("prefix.json", "w") as f:
		json.dump(prefix_list, fp=f, indent=4)
	try:
		return prefix_list[str(message.guild.id)]["prefix"]
	except AttributeError:
		return list(PREFIX.split(" "))


bot = commands.Bot(command_prefix=get_prefix)
bot.start_time = datetime.datetime.utcnow()
bot.prefix_default = PREFIX.split(" ")
bot.users_json = USERS_FILE
bot.prefix_json = PREFIX_FILE
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send("Command Not found!")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("You don't have enough permissions.")
	elif isinstance(error, commands.CheckAnyFailure):
		await ctx.send("".join(error.args))
	elif isinstance(error, commands.PrivateMessageOnly):
		await ctx.send("You're only allowed to use this command in Direct or Private Message only!")
	elif isinstance(error, commands.NotOwner):
		await ctx.send("You're not a owner till now!")
	elif isinstance(error, commands.NoPrivateMessage):
		await ctx.send("You can't send this commands here!")
	elif isinstance(error, commands.CommandOnCooldown):
		await ctx.send("The command you send is on cooldown!")
	else:
		raise error


@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name=f"OpenCity • Type {random.choice(bot.prefix_default)}help to get started"))
	# guild = discord.utils.get(client.guildTry .helps, id=GUILD_ID)
	roles_needed = ["Muted Members", "Banned Members", "Kicked Members"]
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


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		bot.load_extension(f'cogs.{filename[:-3]}')


@tasks.loop(hours=1)
async def my_presence_per_day():
	await bot.wait_until_ready()
	await bot.change_presence(activity=discord.Game(name=f"OpenCity • Type {random.choice(bot.prefix_default)}help to get started"))
	print("changed")


@bot.command()
@commands.is_owner()
async def reload_all_extensions(ctx):
	for filename1 in os.listdir('./cogs'):
		if filename1.endswith('.py'):
			bot.unload_extension(f'cogs.{filename1[:-3]}')
			bot.load_extension(f'cogs.{filename1[:-3]}')
	await ctx.send("Reloaded all extensions!")


my_presence_per_day.start()

bot.run(TOKEN)
