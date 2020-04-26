__author__ = ["Sairam", "NameKhan72"]

import asyncio

import discord
from discord.ext import commands


class Direct_Message_Support(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.welcome_message = (
			'Hello, welcome to the {} Discord-server! \n \n I can answer most of your questions.\n Most of the question can be answered by reading faq though!! 😀 \nYou can ask me if you want: \n\
						\n\
							1: What is this? or what is the server meant for?\n \
							2: Who is the administrator? or owner?\n \
							3: When will OpenCity be released?\n \
							4: How far are the game has progressed so far?\n \
							5: Who made this bot?\n \
							6: What is this game?\n \
							7: What will be the specifications?\n \
							8: What is premium subscription?\n \
							9: What is Special Sandbox subscription?\n \
							10: What is the use of diamonds?\n \
							11: Do you have any price map for subscriptions?\n \
							To ask me just type in the number in front of the question!'
		)
		self.questions = (
			'I can answer most of your questions.\n Most of the question can be answered by reading faq though!! 😀 \n You can ask me if you want: \n \
			\n \
			1: What is this? or what is the server meant for ?\n \
			2: Who is the administrator? or owner?\n \
			3: When will OpenCity be released?\n \
			4: How far are the game has progressed so far?\n \
			5: Who made this bot?\n \
			6: What is this game?\n \
			7: What will be the specifications?\n \
			8: What is premium subscription?\n \
			9: What is Special Sandbox subscription?\n \
			10: What is the use of diamonds?\n \
			11: Do you have any price map for subscriptions?\n \
			To ask me just type in the number in front of the question!'
		)
		self.response_dict = {
			1: 'This is the support discord for the OpenCity city building game.',
			2: 'Sairam',
			3: "We don't have any ETA for now, we'll let you know",
			4: 'We have made Main Menu and some icons',
			5: 'NameKhan72, Sairam, Wizard BINAY',
			6: 'The game OpenCity is the city simulation and transport simulation with first person view of your city and drivable road vehicles, trains, ships and aircrafts.',
			7: 'We are not able to answer, but we can spectate.\
```\
OS: Windows 10 1909 or Above 64-Bit, MacOS 10.15 or Above, Linux Debian, Linux Mint or Ubuntu\n\
CPU: Core i5 or greater\n\
RAM: 4GB or Above\n\
GPU: 2GB or Above\n\
Storage: 12GB\
```',
			8: 'Premium is a subscription of OpenCity, it contains assets and features which are very difficult for developers to make.',
			9: 'Special Sandbox is also a subscription, which is a superset of built-in sandbox, it is named as "Everything Unlimited", as it makes all the currencies unlimited.',
			10: 'Diamonds are used to get parts of premium subscription.',
			11: 'We don\'t have any price map for the subscriptions.'

		}

	@commands.Cog.listener()
	async def on_member_join(self, member: discord.Member):
		guild = member.guild
		await member.create_dm()
		await member.dm_channel.send(self.welcome_message.format(guild.name))

	# @commands.Cog.listener()
	# async def on_message(self, message: discord.Message):
	# 	if message.author == self.bot.user:
	# 		return
	# 	if message.channel.type == discord.ChannelType.private:
	# 		if not str(message.content).startswith("!"):
	# 			async with message.channel.typing():
	# 				if int(message.content) in self.response_dict.keys():
	# 					try:
	# 						await message.channel.send(self.response_dict[int(message.content)])
	# 					except ValueError:
	# 						await message.channel.send("You send a wrong message")
	# 				else:
	# 					await message.channel.send(f"Sorry we just have {len(self.response_dict.keys())} questions as FAQ. More will be added.")

	@commands.command()
	async def support(self, ctx: commands.Context):
		await ctx.send(self.questions)

		def check(message: discord.Message) -> bool:
			return message.author == ctx.author

		while True:
			try:
				response_by_user = await self.bot.wait_for('message', check=check, timeout=60)
			except asyncio.TimeoutError:
				await ctx.send("You took to long to respond")
				break
			else:
				if ctx.channel.type == discord.ChannelType.private:
					if int(response_by_user.content) in self.response_dict.keys():
						async with ctx.channel.typing():
							try:
								await ctx.send(self.response_dict[int(response_by_user.content)])
							except ValueError:
								await ctx.send("You sent a wrong message")
					else:
						await ctx.send(f"Sorry we just have {len(self.response_dict.keys())} questions as FAQ. More will be added.")


def setup(bot):
	bot.add_cog(Direct_Message_Support(bot))
