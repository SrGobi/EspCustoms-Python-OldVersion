import asyncio
import discord
from discord.ext import commands

color_main = discord.Color(0xF5F5F5)
color_done = discord.Color(0x00FFFF)
color_warn = discord.Color(0xFFFF00)
color_errr = discord.Color(0xFF0000)

emoji_loading = "<a:EspLoading:792360430491402240>"

class working(commands.Cog):
    def __init__(self, discord_bot):
        self.discord_bot = discord_bot

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def working(self, ctx):
        author = ctx.author
        icon = ctx.guild.icon_url
        embe=discord.Embed(title="ESP CUSTOMS", description=f"━━━━━━━ {emoji_loading}・Maintenance ・{emoji_loading} ━━━━━━━", color=color_main)
        embe.add_field(name="Verification FN", value="Working", inline=True)
        embe.add_field(name="Customs FN", value="Working", inline=True)
        embe.add_field(name="Custom Commands", value="Working", inline=True)
        embe.add_field(name="Premium", value="Working", inline=True)
        embe.add_field(name="Dashboard", value="Working", inline=True)
        embe.add_field(name="Torunaments", value="Working", inline=True)
        embe.set_thumbnail(url=icon)
        embe.set_footer(text=f"Host: {author} | Made with BLD SRGOBI#5100")
        message = await ctx.send(embed=embe)
        while True:
            await asyncio.sleep(5)
            embe_1=discord.Embed(title="ESP CUSTOMS", description=f"━━━━━━━ {emoji_loading}・Maintenance ・{emoji_loading} ━━━━━━━", color=color_main)
            embe_1.add_field(name="Verification FN", value="Working.", inline=True)
            embe_1.add_field(name="Customs FN", value="Working.", inline=True)
            embe_1.add_field(name="Custom Commands", value="Working.", inline=True)
            embe_1.add_field(name="Premium", value="Working.", inline=True)
            embe_1.add_field(name="Dashboard", value="Working.", inline=True)
            embe_1.add_field(name="Torunaments", value="Working.", inline=True)
            embe_1.set_thumbnail(url=icon)
            embe_1.set_footer(text=f"Host: {author} | Made with BLD SRGOBI#5100")
            await message.edit(embed=embe_1)
            await asyncio.sleep(5)
            embe_2=discord.Embed(title="ESP CUSTOMS", description=f"━━━━━━━ {emoji_loading}・Maintenance ・{emoji_loading} ━━━━━━━", color=color_main)
            embe_2.add_field(name="Verification FN", value="Working..", inline=True)
            embe_2.add_field(name="Customs FN", value="Working..", inline=True)
            embe_2.add_field(name="Custom Commands", value="Working..", inline=True)
            embe_2.add_field(name="Premium", value="Working..", inline=True)
            embe_2.add_field(name="Dashboard", value="Working..", inline=True)
            embe_2.add_field(name="Torunaments", value="Working..", inline=True)
            embe_2.set_thumbnail(url=icon)
            embe_2.set_footer(text=f"Host: {author} | Made with BLD SRGOBI#5100")
            await message.edit(embed=embe_2)
            await asyncio.sleep(5)
            embe_3=discord.Embed(title="ESP CUSTOMS", description=f"━━━━━━━ {emoji_loading}・Maintenance ・{emoji_loading} ━━━━━━━", color=color_main)
            embe_3.add_field(name="Verification FN", value="Working...", inline=True)
            embe_3.add_field(name="Customs FN", value="Working...", inline=True)
            embe_3.add_field(name="Custom Commands", value="Working...", inline=True)
            embe_3.add_field(name="Premium", value="Working...", inline=True)
            embe_3.add_field(name="Dashboard", value="Working...", inline=True)
            embe_3.add_field(name="Torunaments", value="Working...", inline=True)
            embe_3.set_thumbnail(url=icon)
            embe_3.set_footer(text=f"Host: {author} | Made with BLD SRGOBI#5100")
            await message.edit(embed=embe_3)
            


def setup(discord_bot):
    discord_bot.add_cog(working(discord_bot))
    print('WORKING')