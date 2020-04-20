import discord
import random
import json
from Bot.color_builder import color_dict2discord_color_list

TOKEN = 'NjkzNDAxNjcxODM2ODkzMjM1.Xpb63Q.fyUesqYViFssI6VaT1S2814Zb0w'

bot = discord.Client()


@bot.event
async def on_ready():
	print(f"{bot.user} has connected to Discord!")


@bot.event
async def on_message(message):
	if discord.utils.find(lambda r: r.name == 'Respected People', message.guild.roles) in message.guild.roles:
		pass
	else:
		await message.guild.create_role(name="Respected People", color=discord.colour.Colour(0x8600ff), hoist=True, mentionable=True)

	if message.channel.type != discord.ChannelType.private:
		if discord.utils.find(lambda r: r.name == 'Respected People', message.guild.roles) not in message.author.roles and message.author.bot is False:

			with open('users.json', 'r') as file:
				file_data = json.load(file)
			if str(message.guild.id) not in file_data.keys():
				file_data[str(message.guild.id)] = {}
			if str(message.author.id) not in file_data[str(message.guild.id)].keys():
				file_data[str(message.guild.id)][str(message.author.id)] = {'xps': 0}
			file_data[str(message.guild.id)][str(message.author.id)]['xps'] += random.randrange(5, 25, 5)
			user_xps = file_data[str(message.guild.id)][str(message.author.id)]['xps']
			with open('users.json', 'w') as file:
				file.write(json.dumps(file_data, indent=4))

			xps_level = [0, 55, 195, 255, 365, 655, 965, 1225, 2565, 3655, 9665]

			leveling_prefix = ['Pl. ', 'New ', 'Very Tiny ', 'Tiny ', 'Small ', '', 'Big ', 'Huge ', 'Very Huge ', 'Old ', 'Fl. ']
			leveling_roles = {'admin': ['Administrators', []], 'mod': ['Moderators', []], 'citizen': ['OpenCitizens', []]}

			color_dict = {
				"red": ["#DC143C", "#8B0000"],
				"yellow": ["#FFFF99", "#666600"],
				"green": ["#90EE90", "#006400"]
			}
			leveling_prefix_1 = list(reversed(leveling_prefix))
			list_of_discord_colors = color_dict2discord_color_list(color_dict)
			user_category = None
			for i, list_of_discord_color in zip(leveling_roles, list_of_discord_colors):
				for (j, k), color_1 in zip(enumerate(leveling_prefix), list_of_discord_color):
					# await discord.utils.get(message.guild.roles, name=leveling_prefix[j] + leveling_roles[i][0]).delete()
					# await message.guild.create_role(name=leveling_prefix[j] + leveling_roles[i][0], color=color_1)
					if discord.utils.get(message.guild.roles, name=leveling_prefix_1[j] + leveling_roles[i][0]):
						if discord.utils.find(lambda r: r.name == leveling_prefix[0] + leveling_roles[i][0], message.guild.roles) in message.author.roles:
							user_category = i
							break
					else:
						# pass
						await message.guild.create_role(name=leveling_prefix_1[j] + leveling_roles[i][0], color=color_1, hoist=True, mentionable=True)
			if user_category is None:
				await message.author.add_roles(discord.utils.find(lambda r: r.name == leveling_prefix[0] + leveling_roles['citizen'][0], message.guild.roles))
				user_category = 'citizen'

			for i in range(len(xps_level)):
				if discord.utils.get(message.guild.roles, name=leveling_prefix[i] + leveling_roles[user_category][0]):
					leveling_roles[user_category][1].append(discord.utils.find(lambda r: r.name == leveling_prefix[i] + leveling_roles[user_category][0], message.guild.roles))
				else:
					leveling_prefix.reverse()
					await message.guild.create_role(name=leveling_prefix[i] + leveling_roles[user_category][0])
					leveling_prefix.reverse()
					leveling_roles[user_category][1].append(discord.utils.find(lambda r: r.name == leveling_prefix[i] + leveling_roles[user_category][0], message.guild.roles))

			if user_xps < xps_level[1]:
				new_user_level = 0
			elif xps_level[1] <= user_xps < xps_level[-1]:
				for i in range(1, len(xps_level) - 1):
					if xps_level[i] <= user_xps < xps_level[i + 1]:
						new_user_level = i
						break
			else:
				new_user_level = len(xps_level) - 1
			if discord.utils.find(lambda r: r.name == leveling_prefix[new_user_level] + leveling_roles[user_category][0], message.guild.roles) not in message.author.roles:
				await message.author.add_roles(discord.utils.find(lambda r: r.name == leveling_prefix[new_user_level] + leveling_roles[user_category][0], message.guild.roles))

	if message.content.startswith('!myxps'):
		if discord.utils.find(lambda r: r.name == 'Respected People', message.guild.roles) in message.author.roles:
			await message.channel.send(f"<@{message.author.id}> you are a Respected People or you have finished leveling")
		else:
			await message.channel.send(f"<@{message.author.id}> you have {user_xps}xps!")

	if message.content.startswith('!viewxps'):
		if len(message.mentions) > 0:
			with open('users.json', 'r') as file:
				file_data = json.load(file)
			msg = ''
			for i in message.mentions:
				if not i.bot:
					if discord.utils.find(lambda r: r.name == 'respected people', message.guild.roles) in i.roles:
						msg += f"<@{i.id}> is a respected people.\n"
					else:
						if str(i.id) not in file_data[str(message.guild.id)].keys():
							file_data[str(message.guild.id)][str(i.id)] = {'xps': 0}
						user_xps = file_data[str(message.guild.id)][str(i.id)]['xps']
						msg += f"<@{i.id}> has {user_xps}xps.\n"
				else:
					msg += f"<@{i.id}> is a Bot.\n"
			with open('users.json', 'w') as file:
				file.write(json.dumps(file_data, indent=4))
			await message.channel.send(msg)
		else:
			await message.channel.send('<@' + str(message.author.id) + '> Please mention someone!')


@bot.event
async def on_member_update(before, after):
	leveling_prefix = ['Pl. ', 'New ', 'Very Tiny ', 'Tiny ', 'Small ', '', 'Big ', 'Huge ', 'Very Huge ', 'Old ', 'Fl. ']
	leveling_roles = {'admin': ['Administrators', []], 'mod': ['Moderators', []], 'citizen': ['OpenCitizens', []]}
	base_roles = [leveling_prefix[0] + leveling_roles[i][0] for i in leveling_roles]
	if discord.utils.find(lambda r: r.name == 'Respected People', after.guild.roles) not in after.roles:
		if len(before.roles) < len(after.roles):
			new_role = next(role for role in after.roles if role not in before.roles)
			if after.bot is True and new_role.name in [j + leveling_roles[i][0] for i in leveling_roles for j in leveling_prefix]:
				await after.remove_roles(new_role)
			elif new_role.name in base_roles:
				# set user xps to 0
				with open('users.json', 'r') as file:
					file_data = json.load(file)
				if str(after.guild.id) not in file_data.keys():
					file_data[str(after.guild.id)] = {}
				if str(after.id) not in file_data[str(after.guild.id)].keys():
					file_data[str(after.guild.id)][str(after.id)] = {'xps': 0}
				file_data[str(after.guild.id)][str(after.id)]['xps'] = 0
				with open('users.json', 'w') as file:
					file.write(json.dumps(file_data, indent=4))
				rmrole = list(leveling_roles.keys())[base_roles.index(new_role.name)]
				await after.add_roles(discord.utils.find(lambda r: r.name == leveling_prefix[0] + leveling_roles[rmrole][0], after.guild.roles))
				for i in base_roles:
					if discord.utils.find(lambda r: r.name == i, after.guild.roles) in after.roles and new_role.name != i:
						await after.remove_roles(discord.utils.find(lambda r: r.name == i, after.guild.roles))
			if new_role.name in [leveling_prefix[-1] + leveling_roles[i][0] for i in leveling_roles]:
				rpstat = True
				for i in leveling_roles:
					if discord.utils.find(lambda r: r.name == leveling_prefix[-1] + leveling_roles[i][0], after.guild.roles) not in after.roles:
						rpstat = False
				if rpstat is True:
					# you can set member out of leveling system but it checks with role name "respected people"
					if discord.utils.get(after.guild.roles, name='Respected People'):
						await after.add_roles(discord.utils.find(lambda r: r.name == 'Respected People', after.guild.roles))
					else:
						await after.guild.create_role(name='Respected People')
						await after.add_roles(discord.utils.find(lambda r: r.name == 'Respected People', after.guild.roles))
					for i in leveling_roles:
						for j in leveling_prefix:
							if discord.utils.get(after.guild.roles, name=j + leveling_roles[i][0]) in after.roles:
								await after.remove_roles(discord.utils.find(lambda r: r.name == j + leveling_roles[i][0], after.guild.roles))

		elif len(before.roles) > len(after.roles):
			removed_role = next(role for role in before.roles if role not in after.roles)
			if removed_role.name in [leveling_prefix[0] + leveling_roles[i][0] for i in leveling_roles]:
				rmrole = list(leveling_roles.keys())[base_roles.index(removed_role.name)]
				for i in range(len(leveling_prefix) - 1):
					reqrole = discord.utils.get(after.guild.roles, name=leveling_prefix[i] + leveling_roles[rmrole][0])
					if reqrole and reqrole in after.roles:
						await after.remove_roles(reqrole)


bot.run(TOKEN)
