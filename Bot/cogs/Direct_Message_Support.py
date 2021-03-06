__author__ = ["Sairam", "NameKhan72"]

import asyncio
import json

import discord
from discord.ext import commands


class Direct_Message_Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_message = (
            'Hello, welcome to the {} Discord-server! \n{questions}'
        )
        self.questions_list = [
            '1: What is this? or what is the server meant for?',
            '2: Who is the administrator? or owner?',
            '3: When will OpenCity be released?',
            '4: How far are the game has progressed so far?',
            '5: Who made this bot?',
            '6: What is this game?',
            '7: What will be the specifications?',
            '8: What is premium subscription?',
            '9: What is Special Sandbox subscription?',
            '10: What is the use of diamonds?',
            '11: Do you have any price map for subscriptions?',
        ]
        self.questions = (
            'I can answer most of your questions.\nMost of the question can be answered by reading faq though!! 😀 \nYou can ask me if you want: '
            '```{}```'
            'To ask me just type in the number in front of the question!'.format('\n'.join(self.questions_list))
        )
        self.specification = [
            'OS: Windows 10 1909 or Above 64-Bit, MacOS 10.15 or Above, Linux Debian, Linux Mint or Ubuntu',
            'CPU: Core i5 or greater',
            'RAM: 4GB or Above',
            'GPU: 2GB or Above',
            'Storage: 12GB'
        ]
        self.response_dict = {
            1: 'This is the support discord for the OpenCity city building game.',
            2: 'Sairam',
            3: "We don't have any ETA for now, we'll let you know",
            4: 'We have made Main Menu and some icons',
            5: 'NameKhan72, Sairam, Wizard BINAY, SQWiperYT',
            6: 'The game OpenCity is the city simulation and transport simulation with first person view of your city and drivable road vehicles, trains, ships and aircrafts.',
            7: 'We are not able to answer, but we can spectate.```{}```'.format('\n'.join(self.specification)),
            8: 'Premium is a subscription of OpenCity, it contains assets and features which are very difficult for developers to make.',
            9: 'Special Sandbox is also a subscription, which is a superset of built-in sandbox, it is named as "Everything Unlimited", as it makes all the currencies unlimited.',
            10: 'Diamonds are used to get parts of premium subscription.',
            11: 'We don\'t have any price map for the subscriptions.'

        }

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild_data = json.load(open(self.bot.guilds_json))
        enabled = guild_data[str(member.guild.id)]["enabled"]
        if f"Bot.cogs.{self.qualified_name}" in enabled:
            if not member.bot:
                await member.send(self.welcome_message.format(member.guild.name, questions=self.questions))

    async def cog_check(self, ctx):
        if ctx.channel.type == discord.ChannelType.private:
            return True
        if await self.bot.is_owner(ctx.author):
            return True
        guild_data = json.load(open(self.bot.guilds_json))
        enabled = guild_data[str(ctx.guild.id)]["enabled"]
        return f"Bot.cogs.{self.qualified_name}" in enabled

    @commands.command(help="Gives answers for your question about OpenCity!")
    async def support(self, ctx: commands.Context):
        await ctx.send(self.questions)

        def check(message: discord.Message) -> bool:
            return message.author == ctx.author

        while True:
            try:
                response_by_user = await self.bot.wait_for('message', check=check, timeout=60)
            except asyncio.TimeoutError:
                await ctx.send(f"You took too long to respond {ctx.author.mention}")
                break
            else:
                try:
                    if ctx.channel.type == discord.ChannelType.private:
                        pass
                    if int(response_by_user.content) in self.response_dict.keys():
                        async with ctx.channel.typing():
                            await ctx.send(f"{self.response_dict[int(response_by_user.content)]} {ctx.author.mention}".replace('    ', '').strip())
                    elif int(response_by_user.content) == 0:
                        async with ctx.channel.typing():
                            await ctx.send(f"Great! You found a bug!! {ctx.author.mention}")
                    elif len(self.response_dict.keys()) < int(response_by_user.content) <= 20:
                        async with ctx.channel.typing():
                            await ctx.send(f"Sorry, we just have {len(self.response_dict.keys())} questions as FAQ. More will be added. {ctx.author.mention}")
                    elif 20 < int(response_by_user.content) <= 25:
                        async with ctx.channel.typing():
                            await ctx.send(f"Please don't expect me to answer your questions where the question number is more than 20! {ctx.author.mention}")
                    elif 25 < int(response_by_user.content) <= 90:
                        async with ctx.channel.typing():
                            await ctx.send(f"Stop now! {ctx.author.mention}")
                    else:
                        async with ctx.channel.typing():
                            await ctx.send(f"Okay! {ctx.author.mention} I give up! Please don't disturb now!")
                            break
                except ValueError:
                    if not str(response_by_user).startswith('<') and str(response_by_user).endswith('>'):
                        await ctx.send(f"You sent a wrong message! {ctx.author.mention}")


def setup(bot):
    bot.add_cog(Direct_Message_Support(bot))
