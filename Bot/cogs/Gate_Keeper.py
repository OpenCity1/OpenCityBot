import json
from typing import Union

import discord
from discord.ext import commands


class Gate_Keeper(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if ctx.channel.type == discord.ChannelType.private:
            return True
        guild_data = json.load(open(self.bot.guilds_json))
        enabled = guild_data[str(ctx.guild.id)]["enabled"]
        if f"Bot.cogs.{self.qualified_name}" in enabled:
            return True
        return False

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        pass

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        pass

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: Union[discord.User, discord.Member]):
        pass


def setup(bot):
    bot.add_cog(Gate_Keeper(bot))
