import json
import os
import random
import time
from typing import Optional

import discord
from discord.ext import commands

from Bot.color_builder import color_dict2discord_color_list
from Bot.numbers import make_ordinal


class Leveling(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.xps_level = [0, 55, 195, 255, 365, 655, 965, 1225, 2565, 3655, 9665]

		self.leveling_prefix = ['Pl. ', 'New ', 'Very Tiny ', 'Tiny ', 'Small ', '', 'Big ', 'Huge ', 'Very Huge ', 'Old ', 'Fl. ']
		self.leveling_roles = {'admin': ['Administrators', []], 'mod': ['Moderators', []], 'citizen': ['OpenCitizens', []]}

		self.color_dict = {
			"red": ["#FF5757", "#850000"],
			"yellow": ["#FFFF70", "#757501"],
			"green": ["#73FF73", "#007800"]
		}
		self.file_data = json.load(open(os.path.dirname(__file__) + '/../users.json', "r+"))

		self.base_roles = [self.leveling_prefix[0] + self.leveling_roles[i][0] for i in self.leveling_roles]

	def get_data(self, message):
		with open(os.path.dirname(__file__) + '/../users.json', "r+") as file:
			self.file_data = json.load(file)
			if str(message.guild.id) not in self.file_data.keys():
				self.file_data[str(message.guild.id)] = {}
			if str(message.author.id) not in self.file_data[str(message.guild.id)].keys():
				self.file_data[str(message.guild.id)][str(message.author.id)] = {'xps': 0, 'level': 0, 'last_message': 0}

	def set_data(self):
		with open(os.path.dirname(__file__) + '/../users.json', "w+") as file:
			file.write(json.dumps(self.file_data, indent=4))

	def get_level(self, member: discord.Member):
		return self.file_data[str(member.guild.id)][str(member.id)]['level']

	def get_xps(self, member: discord.Member):
		return self.file_data[str(member.guild.id)][str(member.id)]['xps']

	def update_level(self, message):
		user_xps = self.get_xps(message.author)
		new_user_level = 0
		if user_xps < self.xps_level[1]:
			new_user_level = 0
		elif self.xps_level[1] <= user_xps < self.xps_level[-1]:
			for i in range(1, len(self.xps_level) - 1):
				if self.xps_level[i] <= user_xps < self.xps_level[i + 1]:
					new_user_level = i
					break
		else:
			new_user_level = len(self.xps_level) - 1
		self.file_data[str(message.guild.id)][str(message.author.id)]['level'] = new_user_level

	def update_xps(self, message):
		if (int(time.time()) - self.file_data[str(message.guild.id)][str(message.author.id)]["last_message"]) > 1:
			self.file_data[str(message.guild.id)][str(message.author.id)]['xps'] += random.randrange(5, 25, 5)
			self.file_data[str(message.guild.id)][str(message.author.id)]["last_message"] = int(time.time())

	async def return_user_category(self, message):
		leveling_prefix_1 = list(reversed(self.leveling_prefix))
		list_of_discord_colors = color_dict2discord_color_list(self.color_dict)
		user_category = None
		for i, list_of_discord_color in zip(self.leveling_roles, list_of_discord_colors):
			for (j, k), color_1 in zip(enumerate(self.leveling_prefix), list_of_discord_color):
				# await discord.utils.get(message.guild.roles, name=leveling_prefix[j] + leveling_roles[i][0]).delete()
				# await message.guild.create_role(name=leveling_prefix[j] + leveling_roles[i][0], color=color_1)
				if discord.utils.get(message.guild.roles, name=leveling_prefix_1[j] + self.leveling_roles[i][0]):
					if discord.utils.find(lambda r: r.name == self.leveling_prefix[0] + self.leveling_roles[i][0], message.guild.roles) in message.author.roles:
						user_category = i
						break
		if user_category is None:
			await message.author.add_roles(discord.utils.find(lambda r: r.name == self.leveling_prefix[0] + self.leveling_roles['citizen'][0], message.guild.roles))
			user_category = 'citizen'
		return user_category

	async def give_roles_according_to_level(self, user_category, message):
		user_level = self.get_level(message.author)
		if discord.utils.find(lambda r: r.name == self.leveling_prefix[user_level] + self.leveling_roles[user_category][0], message.guild.roles) not in message.author.roles:
			await message.author.add_roles(discord.utils.find(lambda r: r.name == self.leveling_prefix[user_level] + self.leveling_roles[user_category][0], message.guild.roles))

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.channel.type != discord.ChannelType.private:
			self.get_data(message)
			if discord.utils.find(lambda r: r.name == 'Respected People', message.guild.roles) not in message.author.roles and message.author.bot is False:
				user_category_1 = await self.return_user_category(message)
				self.update_xps(message)
				self.update_level(message)
				await self.give_roles_according_to_level(user_category_1, message)
				self.set_data()

	async def check_new_role(self, before, after):
		new_role = next(role for role in after.roles if role not in before.roles)
		if after.bot is True and new_role.name in [j + self.leveling_roles[i][0] for i in self.leveling_roles for j in self.leveling_prefix]:
			await after.remove_roles(new_role)
		elif new_role.name in self.base_roles:
			# set user xps to 0
			self.file_data[str(after.guild.id)][str(after.id)]['xps'] = 0
			role_category_1 = list(self.leveling_roles.keys())[self.base_roles.index(new_role.name)]
			await after.add_roles(discord.utils.find(lambda r: r.name == self.leveling_prefix[0] + self.leveling_roles[role_category_1][0], after.guild.roles))
			for i in self.base_roles:
				if discord.utils.find(lambda r: r.name == i, after.guild.roles) in after.roles and new_role.name != i:
					await after.remove_roles(discord.utils.find(lambda r: r.name == i, after.guild.roles))

		return new_role

	async def check_respected_people_status(self, new_role, after):
		if new_role.name in [self.leveling_prefix[-1] + self.leveling_roles[i][0] for i in self.leveling_roles]:
			respected_people_status = True
			for i in self.leveling_roles:
				if discord.utils.find(lambda r: r.name == self.leveling_prefix[-1] + self.leveling_roles[i][0], after.guild.roles) not in after.roles:
					respected_people_status = False
			if respected_people_status is True:
				# you can set member out of leveling system but it checks with role name "respected people"
				if discord.utils.get(after.guild.roles, name='Respected People'):
					await after.add_roles(discord.utils.find(lambda r: r.name == 'Respected People', after.guild.roles))
				else:
					await after.add_roles(discord.utils.find(lambda r: r.name == 'Respected People', after.guild.roles))
				for i in self.leveling_roles:
					for j in self.leveling_prefix:
						if discord.utils.get(after.guild.roles, name=j + self.leveling_roles[i][0]) in after.roles:
							await after.remove_roles(discord.utils.find(lambda r: r.name == j + self.leveling_roles[i][0], after.guild.roles))

	async def check_for_removed_role(self, before, after):
		removed_role = next(role for role in before.roles if role not in after.roles)
		if removed_role.name in [self.leveling_prefix[0] + self.leveling_roles[i][0] for i in self.leveling_roles]:
			role_category = list(self.leveling_roles.keys())[self.base_roles.index(removed_role.name)]
			for i in range(len(self.leveling_prefix) - 1):
				required_role = discord.utils.get(after.guild.roles, name=self.leveling_prefix[i] + self.leveling_roles[role_category][0])
				if required_role and required_role in after.roles:
					await after.remove_roles(required_role)

	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		if discord.utils.find(lambda r: r.name == 'Respected People', after.guild.roles) not in after.roles:
			if len(before.roles) < len(after.roles):
				new_role_1 = await self.check_new_role(before, after)
				await self.check_respected_people_status(new_role_1, after)
			elif len(before.roles) > len(after.roles):
				await self.check_for_removed_role(before, after)

	@commands.command()
	async def xps(self, ctx: commands.Context, member: Optional[discord.Member] = None):
		if member is None:
			user_xps = self.get_xps(ctx.author)
			if discord.utils.find(lambda r: r.name == 'Respected People', ctx.guild.roles) in ctx.author.roles:
				await ctx.send(f"<@{ctx.author.id}> you are a Respected People or you have finished leveling")
			else:
				await ctx.send(f"<@{ctx.author.id}> you have {user_xps}xps!")
		else:
			if len(ctx.message.mentions) > 0:
				msg = ''
				for user in ctx.message.mentions:
					if not user.bot:
						if discord.utils.find(lambda r: r.name == 'Respected People', ctx.guild.roles) in user.roles:
							msg += f"<@{user.id}> is a respected people or have finished leveling.\n"
						else:
							if str(user.id) not in self.file_data[str(ctx.guild.id)].keys():
								self.file_data[str(ctx.guild.id)][str(user.id)] = {'xps': 0}
							user_xps = self.file_data[str(ctx.guild.id)][str(user.id)]['xps']
							msg += f"<@{user.id}> has {user_xps}xps.\n"
					else:
						msg += f"<@{user.id}> is a Bot.\n"
				await ctx.send(msg)
			else:
				await ctx.send('<@' + str(ctx.author.id) + '> Please mention someone!')

	@commands.command()
	async def level(self, ctx: commands.Context, member: Optional[discord.Member] = None):
		if member is None:
			user_level = self.get_level(ctx.author)
			if discord.utils.find(lambda r: r.name == 'Respected People', ctx.guild.roles) in ctx.author.roles:
				await ctx.send(f"<@{ctx.author.id}> you are a Respected People or you have finished leveling.")
			else:
				await ctx.send(f"<@{ctx.author.id}> you are in {make_ordinal(user_level)} level!")
		else:
			if len(ctx.message.mentions) > 0:
				msg = ''
				for user in ctx.message.mentions:
					if not user.bot:
						if discord.utils.find(lambda r: r.name == 'Respected People', ctx.guild.roles) in user.roles:
							msg += f"<@{user.id}> is a respected people or have finished leveling.\n"
						else:
							if str(user.id) not in self.file_data[str(ctx.guild.id)].keys():
								self.file_data[str(ctx.guild.id)][str(user.id)] = {'level': 0}
							user_level = self.file_data[str(ctx.guild.id)][str(user.id)]['level']
							msg += f"<@{user.id}> is in {make_ordinal(user_level)} level.\n"
					else:
						msg += f"<@{user.id}> is a Bot.\n"
				await ctx.send(msg)
			else:
				await ctx.send('<@' + str(ctx.author.id) + '> Please mention someone!')

	@commands.command()
	async def create_roles(self, ctx: commands.Context):
		if discord.utils.find(lambda r: r.name == 'Respected People', ctx.guild.roles) not in ctx.guild.roles:
			await ctx.guild.create_role(name="Respected People", color=discord.colour.Colour(0x8600ff), hoist=True, mentionable=True)
		leveling_prefix_1 = list(reversed(self.leveling_prefix))
		list_of_discord_colors = color_dict2discord_color_list(self.color_dict)
		for i, list_of_discord_color in zip(self.leveling_roles, list_of_discord_colors):
			for (j, k), color_1 in zip(enumerate(self.leveling_prefix), list_of_discord_color):
				if discord.utils.get(ctx.guild.roles, name=leveling_prefix_1[j] + self.leveling_roles[i][0]) not in ctx.guild.roles:
					await ctx.guild.create_role(name=leveling_prefix_1[j] + self.leveling_roles[i][0], color=color_1, hoist=True, mentionable=True)
		await ctx.send("Created All levelling roles")

	@commands.command()
	async def delete_roles(self, ctx: commands.Context):
		if discord.utils.find(lambda r: r.name == 'Respected People', ctx.guild.roles) in ctx.guild.roles:
			await discord.utils.get(ctx.guild.roles, name="Respected People", color=discord.colour.Colour(0x8600ff), hoist=True, mentionable=True).delete()
		leveling_prefix_1 = list(reversed(self.leveling_prefix))
		list_of_discord_colors = color_dict2discord_color_list(self.color_dict)
		for i, list_of_discord_color in zip(self.leveling_roles, list_of_discord_colors):
			for (j, k), color_1 in zip(enumerate(self.leveling_prefix), list_of_discord_color):
				if discord.utils.get(ctx.guild.roles, name=leveling_prefix_1[j] + self.leveling_roles[i][0]) in ctx.guild.roles:
					await discord.utils.get(ctx.guild.roles, name=leveling_prefix_1[j] + self.leveling_roles[i][0], color=color_1, hoist=True, mentionable=True).delete()
		await ctx.send("Deleted All levelling roles")

	@commands.command()
	async def delete_all_roles(self, ctx: commands.Context):
		if discord.utils.find(lambda r: r.name == 'Respected People', ctx.guild.roles) in ctx.guild.roles:
			await discord.utils.get(ctx.guild.roles, name="Respected People").delete()
		leveling_prefix_1 = list(reversed(self.leveling_prefix))
		list_of_discord_colors = color_dict2discord_color_list(self.color_dict)
		for i, list_of_discord_color in zip(self.leveling_roles, list_of_discord_colors):
			for (j, k), color_1 in zip(enumerate(self.leveling_prefix), list_of_discord_color):
				if discord.utils.get(ctx.guild.roles, name=leveling_prefix_1[j] + self.leveling_roles[i][0]) in ctx.guild.roles:
					await discord.utils.get(ctx.guild.roles, name=leveling_prefix_1[j] + self.leveling_roles[i][0]).delete()
		await ctx.send("Deleted All levelling roles")


def setup(bot):
	bot.add_cog(Leveling(bot))
