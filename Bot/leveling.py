import discord
import json

client = discord.Client


async def on_level_up_message(message):
	if not message.author.bot:
		with open('levels.json', 'r') as f:
			users = json.load(f)

		await update_data(users, message.author)
		await add_experience(users, message.author, 5)
		await level_up(users, message.author, message)

		with open('levels.json', 'w') as f:
			json.dump(users, f)


async def update_data(users, user):
	if f'{user.id}'not in users:
		users[f'{user.id}'] = {}
		users[f'{user.id}']['experience'] = 0
		users[f'{user.id}']['level'] = 0


async def add_experience(users, user, exp):
	users[f'{user.id}']['experience'] += exp


async def level_up(users, user, message):
	experience = users[f'{user.id}']['experience']
	lvl_start = users[f'{user.id}']['level']
	lvl_end = int(experience ** (1 / 4))
	if lvl_start < lvl_end:
		await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}')
		users[f'{user.id}']['level'] = lvl_end
