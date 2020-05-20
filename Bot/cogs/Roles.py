import json

import discord
from discord.ext import commands


class Roles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.channel.type == discord.ChannelType.private:
            return True
        if await self.bot.is_owner(ctx.author):
            return True
        guild_data = json.load(open(self.bot.guilds_json))
        enabled = guild_data[str(ctx.guild.id)]["enabled"]
        if f"Bot.cogs.{self.qualified_name}" in enabled:
            return True
        return False

    @commands.group(help="Does nothing when invoked without subcommand")
    async def role(self, ctx: commands.Context):
        pass

    @role.group(name="custom", help="Does nothing when invoked without subcommand")
    async def role_custom(self, ctx: commands.Context):
        pass

    @role.group(name="bot", help="Does nothing when invoked without subcommand")
    async def role_bot(self, ctx: commands.Context):
        pass

    @role.group(name="humans", help="Does nothing when invoked without subcommand")
    async def role_humans(self, ctx: commands.Context):
        pass

    @role.group(name="in", help="Does nothing when invoked without subcommand")
    async def role_in(self, ctx: commands.Context):
        pass

    @role_custom.command(name="add", help="Adds a role to a member!")
    async def role_custom_add(self, ctx: commands.Context, member: discord.Member, role: discord.Role):
        await member.add_roles(role)
        await ctx.send(f"Role {role.mention} added to {member.mention}")

    @role_custom.command(name="remove", help="Removes a role from a member!")
    async def role_custom_remove(self, ctx: commands.Context, member: discord.Member, role: discord.Role):
        await member.remove_roles(role)
        await ctx.send(f"Role {role.mention} removed from {member.mention}")

    @role_bot.command(name="add", help="Adds a role to all bots!")
    async def role_bot_add(self, ctx: commands.Context, role: discord.Role):
        for member in ctx.guild.members:
            if member.bot:
                await member.add_roles(role)

    @role_bot.command(name="remove", help="Removes a role from all bots!")
    async def role_bot_remove(self, ctx: commands.Context, role: discord.Role):
        for member in ctx.guild.members:
            if member.bot:
                await member.remove_roles(role)

    @role_humans.command(name="add", help="Adds a role to all humans!")
    async def role_humans_add(self, ctx: commands.Context, role: discord.Role):
        for member in ctx.guild.members:
            if not member.bot:
                await member.add_roles(role)

    @role_humans.command(name="remove", help="Removes a role from all humans!")
    async def role_humans_remove(self, ctx: commands.Context, role: discord.Role):
        for member in ctx.guild.members:
            if not member.bot:
                await member.remove_roles(role)

    @role_in.command(name="add", help="Adds a role to members in a role!")
    async def role_in_add(self, ctx: commands.Context, in_role: discord.Role, role: discord.Role):
        for member in ctx.guild.members:
            if in_role in member.roles:
                await member.add_roles(role)

    @role_in.command(name="remove", help="Removes a role from members in a role")
    async def role_in_remove(self, ctx: commands.Context, in_role: discord.Role, role: discord.Role):
        for member in ctx.guild.members:
            if in_role in member.roles:
                await member.remove_roles(role)


def setup(bot):
    bot.add_cog(Roles(bot))
