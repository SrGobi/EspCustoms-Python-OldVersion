import asyncio
import discord
from discord.ext import commands

color_main = discord.Color(0xF5F5F5)
color_done = discord.Color(0x00FFFF)
color_warn = discord.Color(0xFFFF00)
color_errr = discord.Color(0xFF0000)

class info(commands.Cog):
    def __init__(self, discord_bot):
        self.discord_bot = discord_bot

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def userinfo(self, ctx, *, user: discord.Member = None):
        em=discord.Embed(title="User information", color=color_main)
        em.set_author(name=str(user), icon_url=user.avatar_url)
        em.add_field(name="ID", value=str(user.id), inline=True)
        await ctx.send(embed=em)

def setup(discord_bot):
    discord_bot.add_cog(info(discord_bot))
    print('USER-INFO')