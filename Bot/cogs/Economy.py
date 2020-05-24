import json
from typing import Optional

import discord
from discord.ext import commands

from Bot.cogs.utils.checks import is_guild_owner


class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    async def cog_check(self, ctx):
        try:
            guild_data = json.load(open(self.bot.guilds_json))
            enabled = guild_data[str(ctx.guild.id)]["enabled"]
            return f"Bot.cogs.{self.qualified_name}" in enabled or await self.bot.is_owner(ctx.author)
        except AttributeError:
            return await self.bot.is_owner(ctx.author)

    @commands.group(invoke_without_command=True)
    async def money(self, ctx):
        formatted_money = ''
        economy_data = json.load(open(self.bot.economy_json, encoding='utf-8'))
        if str(ctx.guild.id) not in economy_data.keys():
            economy_data[str(ctx.guild.id)] = {}
            economy_data[str(ctx.guild.id)]['settings'] = {'currency': 'credits', 'pos': 'back'}
        if str(ctx.author.id) not in economy_data[str(ctx.guild.id)].keys():
            economy_data[str(ctx.guild.id)][str(ctx.author.id)] = {'money': 0}
        if economy_data[str(ctx.guild.id)]['settings']['pos'] == 'back':
            formatted_money = f"{economy_data[str(ctx.guild.id)][str(ctx.author.id)]['money']}{economy_data[str(ctx.guild.id)]['settings']['currency']}"
        if economy_data[str(ctx.guild.id)]['settings']['pos'] == 'front':
            formatted_money = f"{economy_data[str(ctx.guild.id)]['settings']['currency']}{economy_data[str(ctx.guild.id)][str(ctx.author.id)]['money']}"
        await ctx.send(f"You have {formatted_money}")
        json.dump(economy_data, open(self.bot.economy_json, 'w', encoding='utf-8'), indent='\t')

    @money.command(name='add', aliases=['+'])
    @is_guild_owner()
    async def money_add(self, ctx, member: Optional[discord.Member] = None, amount: int = 0):
        member = ctx.author if member is None else member
        economy_data = json.load(open(self.bot.economy_json, encoding='utf-8'))
        if str(ctx.guild.id) not in economy_data.keys():
            economy_data[str(ctx.guild.id)] = {}
            economy_data[str(ctx.guild.id)]['settings'] = {'currency': 'credits', 'pos': 'back'}
        if str(member.id) not in economy_data[str(ctx.guild.id)].keys():
            economy_data[str(ctx.guild.id)][str(member.id)] = {'money': 0}
        economy_data[str(ctx.guild.id)][str(member.id)]['money'] += amount
        json.dump(economy_data, open(self.bot.economy_json, 'w', encoding='utf-8'), indent='\t')

    @money.command(name='remove', aliases=['-'])
    @is_guild_owner()
    async def money_remove(self, ctx, member: Optional[discord.Member] = None, amount: int = 0):
        member = ctx.author if member is None else member
        economy_data = json.load(open(self.bot.economy_json, encoding='utf-8'))
        if str(ctx.guild.id) not in economy_data.keys():
            economy_data[str(ctx.guild.id)] = {'currency': 'credits', 'pos': 'back'}
        if str(member.id) not in economy_data[str(ctx.guild.id)].keys():
            economy_data[str(ctx.guild.id)][str(member.id)] = {'money': 0}
        economy_data[str(ctx.guild.id)][str(member.id)]['money'] -= amount
        json.dump(economy_data, open(self.bot.economy_json, 'w', encoding='utf-8'), indent='\t')

    @money.command(name='set', aliases=['='])
    @is_guild_owner()
    async def money_set(self, ctx, member: Optional[discord.Member] = None, amount: int = 0):
        member = ctx.author if member is None else member
        economy_data = json.load(open(self.bot.economy_json, encoding='utf-8'))
        if str(ctx.guild.id) not in economy_data.keys():
            economy_data[str(ctx.guild.id)] = {}
            economy_data[str(ctx.guild.id)]['settings'] = {'currency': 'credits', 'pos': 'back'}
        if str(member.id) not in economy_data[str(ctx.guild.id)].keys():
            economy_data[str(ctx.guild.id)][str(member.id)] = {'money': 0}
        economy_data[str(ctx.guild.id)][str(member.id)]['money'] = amount
        json.dump(economy_data, open(self.bot.economy_json, 'w', encoding='utf-8'), indent='\t')

    @commands.command(name='set_currency')
    async def currency_set(self, ctx, symbol: Optional[str] = None, pos: Optional[str] = None):
        economy_data = json.load(open(self.bot.economy_json, encoding='utf-8'))
        if str(ctx.guild.id) not in economy_data.keys():
            economy_data[str(ctx.guild.id)] = {}
            economy_data[str(ctx.guild.id)]['settings'] = {'currency': 'credits', 'pos': 'back'}
        old_currency_data = economy_data[str(ctx.guild.id)]['settings']
        new_currency_data: dict = {}
        if symbol is None and pos is None:
            new_currency_data = old_currency_data
        if len(symbol) < 2 and pos is None:
            new_currency_data = {'currency': f'{symbol}', 'pos': 'front'}
        if symbol is not None and pos is not None:
            new_currency_data = {'currency': f'{symbol}', 'pos': f'{pos}'}
        if len(symbol) > 2 and pos is None:
            new_currency_data = {'currency': f'{symbol}', 'pos': 'back'}
        economy_data[str(ctx.guild.id)]['settings'] = new_currency_data
        json.dump(economy_data, open(self.bot.economy_json, 'w', encoding='utf-8'), indent='\t')


def setup(bot):
    bot.add_cog(Economy(bot))
