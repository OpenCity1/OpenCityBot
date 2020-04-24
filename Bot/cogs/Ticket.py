from typing import Union

import discord
from discord.ext import commands


class Ticket(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction: discord.Reaction, user: Union[discord.Member, discord.User]):
		pass


def setup(client):
	client.add_cog(Ticket(client))
