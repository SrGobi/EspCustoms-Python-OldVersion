import asyncio
import discord
from discord.ext import commands

color_main = discord.Color(0xF5F5F5)
color_done = discord.Color(0x00FFFF)
color_warn = discord.Color(0xFFFF00)
color_errr = discord.Color(0xFF0000)

#Crear canal de registro Auditoria
class create_text_channel(commands.Cog):
    def __init__(self, discord_bot):
        self.discord_bot = discord_bot

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def esplog(self, ctx, channelName):
        guild = ctx.guild
        embed_create_chanel = discord.Embed(title=f"Channel Create", description="Now you have to configure the channel permissions and move it to any category if you need it", color=color_main)
        if ctx.author.guild_permissions.manage_channels:
            await guild.create_text_channel(name=channelName)
            await ctx.send(embed=embed_create_chanel)


def setup(discord_bot):
    discord_bot.add_cog(create_text_channel(discord_bot))
    print('ESP-LOG')