from discord.ext import commands
import discord
from core.emojis import Emoji

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Help Page",
                                  description=f"Make http/s requests and get the response FROM DISCORD {Emoji.pog_frog}\nCommands:\n`req get <url>` | Optional keys: `-h`\n`req post <url>`| Optional keys: `-h`, `-d`\n\nTo provide headers use the `-h` key.\nUse the [JSON](https://www.json.org) structure to provide headers and data.\nExample of a request with headers:\n```req get https://example.com -h \"Authorization\": \"123456789\", \"Content-Type\": \"application/json\"```\nWhen using the post command, you can provide body data with the `-d` key\nExample of a post request:\n```req post https://example.com -d Hello!```\nIf you want to send json data then use the same syntax as headers:\n```req post https://example.com -d \"greeting\": \"Hello!\"```",
                                  color=int("00FF00", 16))
            await ctx.send(embed=embed)

    @help.command()
    async def get(self, ctx):
        embed = discord.Embed(title="Get Command",
                              description=f"[`req get <url> (headers)`](https://top.gg/bot/873554215065251840)\n\nMake a GET request to a url.\nExample: ```req get https://example.com```\nExample with headers:\n```req get https://example.com -h \"Authorization\": \"123456789\", \"Content-Type\": \"application/json\"```",
                              color=int("00FF00", 16))
        embed.set_footer(text="<> arguments are required and () arguments are optional")
        await ctx.send(embed=embed)

    @help.command()
    async def post(self, ctx):
        embed = discord.Embed(title="Post Command",
                              description=f"[`req post <url> (headers) (data)`](https://top.gg/bot/873554215065251840)\n\nMake a POST request to a url.\nExample: ```req post https://example.com```\nExample with data and headers:\n```req post https://example.com -d \"greeting\": \"Hello!\" -h \"Authorization\": \"123456789\", \"Content-Type\": \"application/json\"```",
                              color=int("00FF00", 16))
        embed.set_footer(text="<> arguments are required and () arguments are optional")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
