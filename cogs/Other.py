from discord.ext import commands
from discord import Embed
from core.colors import Color

class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        embed = Embed(title="Pong! 🏓", description=f"📡 Bot latency: `{round(self.bot.latency * 1000)}ms`", colour=Color.yellow)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Other(bot))
