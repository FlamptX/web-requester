import os
from dotenv import load_dotenv
import asyncio
import datetime
import difflib
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("TOKEN")

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(*["req "]),
            case_insensitive=True,
            intents=discord.Intents.default(),
            help_command=None
        )

    async def status_task(self):
        while True:
            await asyncio.sleep(3)
            await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                 name='req help in ' + str(
                                                                     len(self.guilds)) + ' servers'))
            await asyncio.sleep(30)
            await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,
                                                                 name='Around'))
            await asyncio.sleep(22)
            await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                                 name='To your requests'))

bot = Bot()

@bot.event
async def on_ready():
    bot.loop.create_task(bot.status_task())

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

    await bot.cogs['Requests'].init_session()

    print('The bot is online')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        lst = []
        for i in bot.commands:
            lst.append(i.name)
        match = difflib.get_close_matches(ctx.message.content.split(' ')[1], lst, n=1)

        if len(match) == 0:
            return
        else:
            await ctx.send(f"Did you make a typo? Did you mean `{match[0]}`?")
        return
    elif isinstance(error, commands.MissingPermissions):
        try:
            await ctx.send("You cannot use this command. Missing `manage messages` permission")
        except Exception:
            print("Bot is missing permission")
        return
    elif isinstance(error.__cause__, discord.Forbidden):
        try:
            await ctx.send("I am missing permissions.")
        except Exception:
            print("Bot is missing permissions.")
        return
    elif isinstance(error, commands.CommandOnCooldown):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        return
    elif isinstance(error, commands.MemberNotFound):
        return
    if ctx.guild.id != 768500204051365888:
        flampt = bot.get_user(621309926631014410) or await bot.fetch_user(621309926631014410)
        embed = discord.Embed(title=":x: Error", colour=discord.Colour.red())
        embed.description = f'```\n{error}\n```'
        embed.timestamp = datetime.datetime.utcnow()
        await flampt.send(embed=embed)
    raise error

bot.run(TOKEN)
