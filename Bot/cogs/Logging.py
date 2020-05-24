import json

import discord
from discord.ext import commands


class Logging(commands.Cog):

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
    async def on_raw_message_delete(self, message):
        pass


def setup(bot):
    bot.add_cog(Logging(bot))
