import asyncio
import discord
from discord.ext import commands

color_main = discord.Color(0xF5F5F5)
color_done = discord.Color(0x00FFFF)
color_warn = discord.Color(0xFFFF00)
color_errr = discord.Color(0xFF0000)

#Say-Embed Discord
class embed(commands.Cog):
    def __init__(self, discord_bot):
        self.discord_bot = discord_bot

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def embed(self, ctx, *, words):
        embed = discord.Embed(color=color_main)
        embed.add_field(name=f"{ctx.author.name}", value=f"{words}" .format(words))
        await ctx.send(embed=embed)


def setup(discord_bot):
    discord_bot.add_cog(embed(discord_bot))
    print('EMBED')