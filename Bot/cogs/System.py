import json
import os

from discord.ext import commands


class System(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.group(aliases=['plugins_all', 'plugin_get_all'])
    async def plugin_all_guild(self, ctx):
        pass

    @plugin_all_guild.command(name="enable", help="Enables given plugin!", aliases=['enable_guild_all', '_+_'])
    async def plugin_enable_all_guild(self, ctx: commands.Context, plugin_ext: str):
        guild_data = json.load(open(self.bot.guilds_json))
        for guild in self.bot.guilds:
            enabled = guild_data[str(guild.id)]["enabled"]
            disabled = guild_data[str(guild.id)]["disabled"]
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
                        enabled.remove("")
                except ValueError:
                    pass
                try:
                    if not disabled:
                        disabled.append("")
                except ValueError:
                    pass
        with open(self.bot.guilds_json, "w+") as f:
            json.dump(guild_data, f, indent='\t')

    @plugin_all_guild.command(name="disable", help="Disables given plugin!", aliases=['disable_guild_all', '_-_'])
    async def plugin_disable_all_guild(self, ctx: commands.Context, plugin_ext: str):
        guild_data = json.load(open(self.bot.guilds_json))
        for guild in self.bot.guilds:
            enabled = guild_data[str(guild.id)]["enabled"]
            disabled = guild_data[str(guild.id)]["disabled"]
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
                        disabled.remove("")
                except ValueError:
                    pass
                try:
                    if not enabled:
                        enabled.append("")
                except ValueError:
                    pass
        with open(self.bot.guilds_json, "w+") as f:
            json.dump(guild_data, f, indent='\t')

    @commands.group(aliases=['ext'])
    async def extension(self, ctx):
        pass

    @extension.command(help="Loads an extension")
    async def load(self, ctx, extension):
        original_dir = os.getcwd()
        os.chdir("../..")
        self.bot.load_extension(f'Bot.cogs.{extension}')
        await ctx.send(f"Loaded {extension}")
        os.chdir(original_dir)

    @extension.command(help="Unloads an extension")
    async def unload(self, ctx, extension):
        original_dir = os.getcwd()
        os.chdir("../..")
        self.bot.unload_extension(f'Bot.cogs.{extension}')
        await ctx.send(f"Unloaded {extension}")
        os.chdir(original_dir)

    @extension.command(help="Reloads an extension")
    async def reload(self, ctx, extension):
        original_dir = os.getcwd()
        os.chdir("../..")
        self.bot.unload_extension(f'Bot.cogs.{extension}')
        self.bot.load_extension(f'Bot.cogs.{extension}')
        await ctx.send(f"Reloaded {extension}")
        os.chdir(original_dir)

    @commands.command(hidden=True)
    async def leave_server(self, ctx: commands.Context):
        await ctx.guild.leave()


def setup(bot):
    bot.add_cog(System(bot))
