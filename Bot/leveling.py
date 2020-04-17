import discord
import json
import random

bot = discord.Client()


async def add_member_to_levels(member):
	with open('levels.json', 'w') as l1:
		json.load(l1)


async def levelling(message):
	if discord.utils.find(lambda r: r.name == 'respected people', message.guild.roles) not in message.author.roles:
		f1 = open("\setup.exe", 'r')
		user_xps = f1
		user_xps += random.randrange(5, 25, 5)

		xps_level = [0, 55, 195, 255, 365, 655, 965, 1225, 2565, 3655, 9665]

		leveling_prefix = ['Pl. ', 'New ', 'Very ', 'Tiny ', 'Small ', '', 'Big ', 'Huge ', 'Very Huge ', 'Old ', 'Fl. ']

		leveling_roles = {'admin': ['Administrators', []], 'mod': ['Moderators', []], 'citizen': ['OpenCitizens', []]}

		user_category = None
		for i in leveling_roles:
			if discord.utils.get(message.guild.roles, name=leveling_prefix[0] + leveling_roles[i][0]):
				if discord.utils.find(lambda r: r.name == leveling_prefix[0] + leveling_roles[i][0], message.guild.roles) in message.author.roles:
					user_category = i
					break
			else:
				await message.guild.create_role(name=leveling_prefix[0] + leveling_roles[i][0])
		if user_category is None:
			await message.author.add_roles(discord.utils.find(lambda r: r.name == leveling_prefix[0] + leveling_roles['citizen'][0], message.guild.roles))
			user_category = 'citizen'

		for i in range(len(xps_level)):
			if discord.utils.get(message.guild.roles, name=leveling_prefix[i] + leveling_roles[user_category][0]):
				leveling_roles[user_category][1].append(discord.utils.find(lambda r: r.name == leveling_prefix[i] + leveling_roles[user_category][0], message.guild.roles))
			else:
				await message.guild.create_role(name=leveling_prefix[i] + leveling_roles[user_category][0])
				leveling_roles[user_category][1].append(discord.utils.find(lambda r: r.name == leveling_prefix[i] + leveling_roles[user_category][0], message.guild.roles))

		if user_xps < xps_level[0]:
			new_user_level = 0
		elif xps_level[1] <= user_xps < xps_level[-1]:
			for i in range(1, len(xps_level) - 1):
				if xps_level[i] <= user_xps < xps_level[i + 1]:
					new_user_level = i
					break
		else:
			new_user_level = len(xps_level) - 1
			# print(new_user_level)
		if discord.utils.find(lambda r: r.name == leveling_prefix[new_user_level] + leveling_roles[user_category][0], message.guild.roles) not in message.author.roles:
			await message.author.add_roles(discord.utils.find(lambda r: r.name == leveling_prefix[new_user_level] + leveling_roles[user_category][0], message.guild.roles))


async def level_update(before, after):
	leveling_prefix = ['Pl. ', 'New ', 'Very ', 'Tiny ', 'Small ', '', 'Big ', 'Huge ', 'Very Huge ', 'Old ', 'Fl. ']
	leveling_roles = {'admin': ['Administrators', []], 'mod': ['Moderators', []], 'citizen': ['OpenCitizens', []]}
	base_roles = [leveling_prefix[0] + leveling_roles[i][0] for i in leveling_roles]
	if discord.utils.find(lambda r: r.name == 'respected people', after.guild.roles) not in after.roles:
		if len(before.roles) < len(after.roles):
			new_role = next(role for role in after.roles if role not in before.roles)
			if new_role.name in base_roles:
				# set user xps to 0
				role_category = list(leveling_roles.keys())[base_roles.index(new_role.name)]
				await after.add_roles(discord.utils.find(lambda r: r.name == leveling_prefix[0] + leveling_roles[role_category][0], after.guild.roles))
				for i in base_roles:
					if discord.utils.find(lambda r: r.name == i, after.guild.roles) in after.roles and new_role.name != i:
						await after.remove_roles(discord.utils.find(lambda r: r.name == i, after.guild.roles))
			if new_role.name in [leveling_prefix[-1] + leveling_roles[i][0] for i in leveling_roles]:
				respected_people_status = True
				for i in leveling_roles:
					if discord.utils.find(lambda r: r.name == leveling_prefix[-1] + leveling_roles[i][0], after.guild.roles) not in after.roles:
						respected_people_status = False
				if respected_people_status is True:
					# you can set member out of leveling system but it checks with role name "respected people"
					if discord.utils.get(after.guild.roles, name='respected people'):
						await after.add_roles(discord.utils.find(lambda r: r.name == 'respected people', after.guild.roles))
					else:
						await after.guild.create_role(name='respected people')
						await after.add_roles(discord.utils.find(lambda r: r.name == 'respected people', after.guild.roles))
					for i in leveling_roles:
						for j in leveling_prefix:
							await after.remove_roles(discord.utils.find(lambda r: r.name == j + leveling_roles[i][0], after.guild.roles))

		elif len(before.roles) > len(after.roles):
			removed_role = next(role for role in before.roles if role not in after.roles)
			if removed_role.name in [leveling_prefix[0] + leveling_roles[i][0] for i in leveling_roles]:
				role_category = list(leveling_roles.keys())[base_roles.index(removed_role.name)]
				for i in range(len(leveling_prefix) - 1):
					required_role = discord.utils.get(after.guild.roles, name=leveling_prefix[i] + leveling_roles[role_category][0])
					if required_role and required_role in after.roles:
						await after.remove_roles(required_role)
