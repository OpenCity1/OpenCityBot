from discord.ext import commands


class Poll(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command()
	async def polls(self, ctx: commands.Context, *, q_and_a):
		question = str(q_and_a).split(", " if ", " in q_and_a else "| ")[0]
		answers = str(q_and_a).split(", " if ", " in q_and_a else "| ")[1:]
		reply = ''
		reply += f"{ctx.author.name}#{ctx.author.discriminator} asks {question}: \n"
		for answer_index, answer in enumerate(answers):
			reply += f"{answer_index}\N{variation selector-16}\N{combining enclosing keycap}: {answer} \n"
		message = await ctx.send(reply)
		for answer_index in range(len(answers)):
			await message.add_reaction(f"{answer_index}\N{variation selector-16}\N{combining enclosing keycap}")


def setup(client):
	client.add_cog(Poll(client))
