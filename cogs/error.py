  
import discord
from discord.ext import commands

color_main = discord.Color(0xF5F5F5)
color_done = discord.Color(0x00FFFF)
color_warn = discord.Color(0xFFFF00)
color_errr = discord.Color(0xFF0000)

class Error(commands.Cog):
    def __init__(self, discord_bot):
        self.discord_bot = discord_bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Basic error handler
        """
        # if command has local error handler, return
        if hasattr(ctx.command, "on_error"):
            return

        # get the original exception
        error = getattr(error, "original", error)

        # command not found
        if isinstance(error, commands.MissingPermissions):
            embed_permissions = discord.Embed(
                title="{}".format("You do not have permission to execute the command"),
                description="",
                color=color_errr,
            )
            await ctx.send(embed=embed_permissions)

        if isinstance(error, commands.CommandNotFound):
            embed_not_found = discord.Embed(
                title="{}".format("Something went wrong"),
                description="",
                color=color_errr,
            )
            embed_not_found.add_field(name="Error", value="Command not found", inline=True)
            await ctx.send(embed=embed_not_found)
            return


def setup(discord_bot):
    discord_bot.add_cog(Error(discord_bot))