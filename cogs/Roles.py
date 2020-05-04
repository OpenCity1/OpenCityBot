from discord.ext import commands


class Roles(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.group(name="role")
	async def _role(self, ctx: commands.Context):
		pass

	@_role.command()
	async def something(self, ctx: commands.Context):
		pass


def setup(bot):
	bot.add_cog(Roles(bot))
