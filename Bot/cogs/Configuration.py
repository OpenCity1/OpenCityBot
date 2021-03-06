import json
from typing import Optional

import discord
from discord.ext import commands

from Bot.cogs.utils.checks import is_guild_owner


class Configuration(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        try:
            return is_guild_owner() or await self.bot.is_owner(ctx.author) or ctx.author
        except AttributeError:
            return await self.bot.is_owner(ctx.author)

    @commands.group(name="prefix", help="Gives you prefixes when sent without subcommands!", invoke_without_command=True)
    async def prefix(self, ctx: commands.Context):
        prefix_list = json.load(open(self.bot.prefix_json))
        embed = discord.Embed()
        embed.title = "Available prefixes for this server!"
        msg = ''
        try:
            for index, item in enumerate(prefix_list[str(ctx.guild.id)]["prefix"]):
                index += 1
                msg += f"{index}. {item}\n"
        except AttributeError:
            for index, item in enumerate(self.bot.prefix_default):
                index += 1
                msg += f"{index}. {item}\n"
        embed.description = msg
        embed.set_author(name=ctx.me.name, icon_url=ctx.me.avatar_url)
        await ctx.send(embed=embed)

    @prefix.command(name="set", help="Sets the prefix for a guild!", aliases=['='])
    @commands.check_any(is_guild_owner(), commands.is_owner())
    async def prefix_set(self, ctx: commands.Context, prefix, index: Optional[int] = 0):
        prefix_list = json.load(open(self.bot.prefix_json))
        prefix_list[str(ctx.guild.id)]["prefix"][index] = prefix
        with open(self.bot.prefix_json, "w") as file:
            json.dump(prefix_list, file, indent='\t')
        await ctx.send(f"Set prefix to {prefix}")

    @prefix.command(name="add", help="Adds a prefix for a guild!", aliases=['+'])
    # @commands.check_any(is_guild_owner(), commands.is_owner())
    @commands.has_guild_permissions(manage_guild=True)
    async def prefix_add(self, ctx: commands.Context, prefix):
        prefix_list = json.load(open(self.bot.prefix_json))
        prefix_list[str(ctx.guild.id)]["prefix"].append(prefix)
        with open(self.bot.prefix_json, "w") as file:
            json.dump(prefix_list, file, indent='\t')
        await ctx.send(f"Added prefix to {prefix}")

    @prefix.command(name="remove", help="Removes the prefix for a guild with index value!", aliases=['-'])
    # @commands.check_any(is_guild_owner(), commands.is_owner())
    @commands.has_guild_permissions(manage_guild=True)
    async def prefix_remove(self, ctx: commands.Context, prefix):
        prefix_list = json.load(open(self.bot.prefix_json))
        prefix_list[str(ctx.guild.id)]["prefix"].remove(prefix)
        with open(self.bot.prefix_json, "w") as file:
            json.dump(prefix_list, file, indent='\t')
        await ctx.send(f"Removed prefix {prefix}")

    @commands.group(name="plugin", help="Shows the enabled plugins for this server!", invoke_without_command=True, aliases=['plugins'])
    async def plugin(self, ctx: commands.Context):
        guild_data = json.load(open(self.bot.guilds_json))
        enabled = guild_data[str(ctx.guild.id)]["enabled"]
        embed = discord.Embed()
        embed.title = "Enabled modules of this server!"
        msg = ''
        for index, item in enumerate(enabled):
            index += 1
            msg += f"{index}. {item.lstrip('Bot.').lstrip('cogs.')}\n"
        embed.description = msg
        embed.set_author(name=ctx.me.name, icon_url=ctx.me.avatar_url)
        await ctx.send(embed=embed)

    @plugin.command(name="enable", help="Enables given plugin!", aliases=['+'])
    # @commands.check_any(is_guild_owner(), commands.is_owner())
    @commands.has_guild_permissions(manage_guild=True)
    async def plugin_enable(self, ctx: commands.Context, plugin_ext: str):
        guild_data = json.load(open(self.bot.guilds_json))
        enabled = guild_data[str(ctx.guild.id)]["enabled"]
        disabled = guild_data[str(ctx.guild.id)]["disabled"]
        plugin_to_enable = f"Bot.cogs.{plugin_ext.replace('_', ' ').title().replace(' ', '_')}"
        if plugin_to_enable in enabled:
            await ctx.send("Plugin already enabled!")
        else:
            try:
                disabled.remove(plugin_to_enable)
            except ValueError:
                pass
            enabled.append(plugin_to_enable)
            await ctx.send("Plugin enabled successfully")
            try:
                if enabled:
                    enabled.remove("None")
            except ValueError:
                pass
            try:
                if not disabled:
                    disabled.append("None")
            except ValueError:
                pass
        with open(self.bot.guilds_json, "w+") as f:
            json.dump(guild_data, f, indent='\t')

    @plugin.command(name="disable", help="Disables given plugin!", aliases=['-'])
    # @commands.check_any(is_guild_owner(), commands.is_owner())
    @commands.has_guild_permissions(manage_guild=True)
    async def plugin_disable(self, ctx: commands.Context, plugin_ext: str):
        guild_data = json.load(open(self.bot.guilds_json))
        enabled = guild_data[str(ctx.guild.id)]["enabled"]
        disabled = guild_data[str(ctx.guild.id)]["disabled"]
        plugin_to_disable = f"Bot.cogs.{plugin_ext.replace('_', ' ').title().replace(' ', '_')}"
        # print(plugin_to_disable)
        if plugin_to_disable in disabled:
            await ctx.send("Plugin already disabled!")
        else:
            try:
                enabled.remove(plugin_to_disable)
            except ValueError:
                pass
            disabled.append(plugin_to_disable)
            await ctx.send("Plugin disabled successfully")
            try:
                if disabled:
                    disabled.remove("None")
            except ValueError:
                pass
            try:
                if not enabled:
                    enabled.append("None")
            except ValueError:
                pass
        with open(self.bot.guilds_json, "w+") as f:
            json.dump(guild_data, f, indent='\t')


def setup(bot):
    bot.add_cog(Configuration(bot))
