import json

import discord
from discord.ext import commands


class Voice_Text_Linking(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.voice_text_data = json.load(open(self.bot.voice_text_json))

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

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        guild_data = json.load(open(self.bot.guilds_json))
        enabled = guild_data[str(member.guild.id)]["enabled"]
        if f"Bot.cogs.{self.qualified_name}" in enabled:
            join_overwrites = {
                member.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, read_message_history=False),
                member: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True)
            }
            leave_overwrites = {
                member.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, read_message_history=False),
                member: discord.PermissionOverwrite(read_messages=False, send_messages=False, read_message_history=False)
            }
            try:
                for voice_channel in self.voice_text_data[str(member.guild.id)]["voice_text"].keys():
                    voice_channel1 = discord.utils.get(member.guild.voice_channels, name=voice_channel)
                    if after.channel == voice_channel1 and before.channel is None:
                        print(f"{member.display_name} joined the voice channel {voice_channel1.name}")
                        channel: discord.TextChannel = discord.utils.get(member.guild.text_channels, name=self.voice_text_data[str(member.guild.id)]["voice_text"][voice_channel])
                        await channel.edit(overwrites=join_overwrites)
                        break
                    if after.channel is None and before.channel == voice_channel1:
                        print(f"{member.display_name} left the voice channel {voice_channel1.name}")
                        channel: discord.TextChannel = discord.utils.get(member.guild.text_channels, name=self.voice_text_data[str(member.guild.id)]["voice_text"][voice_channel])
                        await channel.edit(overwrites=leave_overwrites)
                        await channel.set_permissions(member, overwrite=None)
                        break
                    try:
                        if member.voice.channel == after.channel:
                            print(f"{member.name} switched the voice channel from {before.channel} to {after.channel}")
                            before_channel: discord.TextChannel = discord.utils.get(member.guild.text_channels, name=self.voice_text_data[str(member.guild.id)]["voice_text"][before.channel.name])
                            after_channel: discord.TextChannel = discord.utils.get(member.guild.text_channels, name=self.voice_text_data[str(member.guild.id)]["voice_text"][after.channel.name])
                            await after_channel.edit(overwrites=join_overwrites)
                            await before_channel.edit(overwrites=leave_overwrites)
                            break
                    except AttributeError:
                        pass
            except KeyError:
                pass

    @commands.group(aliases=["vtl", "voice_link"])
    async def voice_text_link(self, ctx):
        if str(ctx.guild.id) not in self.voice_text_data.keys():
            self.voice_text_data[str(ctx.guild.id)] = {}
            self.voice_text_data[str(ctx.guild.id)]["voice_text"] = {}
        embed = discord.Embed()
        embed.title = "Available voice text links!"
        msg = ''
        for index, (key, value) in enumerate(self.voice_text_data[str(ctx.guild.id)]["voice_text"].items()):
            index += 1
            msg += f"{index}. {key} -> {value}\n"
        embed.description = msg
        embed.set_author(name=ctx.me.name, icon_url=ctx.me.avatar_url)
        await ctx.send(embed=embed)
        with open(self.bot.voice_text_json, "w") as f:
            json.dump(self.voice_text_data, f, indent='\t')

    @voice_text_link.command(name="add", help='Creates a new a voice text link')
    async def vtl_add(self, ctx, voice_channel, text_channel):
        voice_channel_1 = discord.utils.get(ctx.guild.voice_channels, name=voice_channel)
        text_channel_1 = discord.utils.get(ctx.guild.text_channels, name=text_channel)
        if str(ctx.guild.id) not in self.voice_text_data.keys():
            self.voice_text_data[str(ctx.guild.id)] = {}
            self.voice_text_data[str(ctx.guild.id)]["voice_text"] = {}
        if (voice_channel_1 or text_channel_1) is None:
            await ctx.send("You didn't send voice channel or text channel!")
        else:
            self.voice_text_data[str(ctx.guild.id)]["voice_text"][voice_channel_1.name] = text_channel_1.name
            await ctx.send(f"Added the voice text link! {voice_channel_1.name} -> {text_channel_1.name}")
        with open(self.bot.voice_text_json, "w") as f:
            json.dump(self.voice_text_data, f, indent='\t')

    @voice_text_link.command(name="remove", help="Deletes a existing voice text link")
    async def vtl_remove(self, ctx, voice_channel):
        if str(ctx.guild.id) not in self.voice_text_data.keys():
            self.voice_text_data[str(ctx.guild.id)] = {}
            self.voice_text_data[str(ctx.guild.id)]["voice_text"] = {}
        voice_channel_1 = discord.utils.get(ctx.guild.voice_channels, name=voice_channel)
        if voice_channel_1 is None:
            await ctx.send("You didn't send voice channel or text channel!")
        else:
            text_channel = self.voice_text_data[str(ctx.guild.id)]["voice_text"].pop(voice_channel_1.name)
            text_channel_1 = discord.utils.get(ctx.guild.text_channels, name=text_channel)
            await ctx.send(f"Removed the voice text link! {voice_channel_1.name} -> {text_channel_1.name}")
        with open(self.bot.voice_text_json, "w") as f:
            json.dump(self.voice_text_data, f, indent='\t')


def setup(bot):
    bot.add_cog(Voice_Text_Linking(bot))
