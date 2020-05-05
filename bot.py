import datetime
import json
import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DEFAULT_PREFIX')


def get_prefix(bot1, message):
	try:
		prefix_list = json.load(open("prefix.json", "r"))
	except (json.JSONDecodeError, FileNotFoundError):
		prefix_list = {}
	if str(message.guild.id) not in prefix_list.keys():
		prefix_list[str(message.guild.id)] = {"prefix": PREFIX}
	with open("prefix.json", "w") as f:
		json.dump(prefix_list, fp=f, indent=4)

	return prefix_list[str(message.guild.id)]["prefix"]


bot = commands.Bot(command_prefix=get_prefix)
bot.start_time = datetime.datetime.utcnow()
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


@bot.event
async def on_command_error(ctx: commands.Context, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send("Command Not found!")
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
	await bot.change_presence(activity=discord.Game(name="OpenCity • Type !help to get started"))
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

bot.run(TOKEN)
