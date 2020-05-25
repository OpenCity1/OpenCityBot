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

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, message):
        pass

    @commands.Cog.listener()
    async def on_raw_message_edit(self, message):
        pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if after.channel is not None and before.channel is None:
            print(f"{member.display_name} joined the voice channel {after.channel.name}")
        if after.channel is None and before.channel is not None:
            print(f"{member.display_name} left the voice channel {before.channel.name}")
        if after.channel == member.voice.channel:
            print(f"{member.name} switched the voice channel from {before.channel} to {after.channel}")


def setup(bot):
    bot.add_cog(Logging(bot))
