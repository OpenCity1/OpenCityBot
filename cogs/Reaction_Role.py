import discord
from discord.ext import commands


class Reaction_Role(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		guild: discord.Guild = self.bot.get_guild(payload.guild_id)
		emoji = payload.emoji
		user: discord.Member = guild.get_member(payload.user_id)
		if str(emoji) == "\U0001f44d":
			role = discord.utils.get(guild.roles, name="Test Role 1")
			await user.add_roles(role)

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		guild: discord.Guild = self.bot.get_guild(payload.guild_id)
		emoji = payload.emoji
		user: discord.Member = guild.get_member(payload.user_id)
		if str(emoji) == "\U0001f44d":
			role = discord.utils.get(guild.roles, name="Test Role 1")
			await user.remove_roles(role)


def setup(bot):
	bot.add_cog(Reaction_Role(bot))
