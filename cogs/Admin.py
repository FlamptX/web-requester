from discord.ext import commands
import discord
import requests
import os
import sys
from time import time

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def resolve_variable(self, variable):
        if hasattr(variable, "__iter__"):
            var_length = len(list(variable))
            if (var_length > 100) and (not isinstance(variable, str)):
                return f"<a {type(variable).__name__} iterable with more than 100 values ({var_length})>"
            elif not var_length:
                return f"<an empty {type(variable).__name__} iterable>"

        if (not variable) and (not isinstance(variable, bool)):
            return f"<an empty {type(variable).__name__} object>"
        return (variable if (
                    len(f"{variable}") <= 1000) else f"<a long {type(variable).__name__} object with the length of {len(f'{variable}'):,}>")

    def prepare(self, string):
        arr = string.strip("```").replace("py\n", "").replace("python\n", "").split("\n")
        if not arr[::-1][0].replace(" ", "").startswith("return"):
            arr[len(arr) - 1] = "return " + arr[::-1][0]
        return "".join(f"\n\t{i}" for i in arr)

    @commands.command(aliases=['exec'], hidden=True)
    @commands.is_owner()
    async def _exec(self, ctx, *, code: str):
        silent = ("-s" in code)

        code = self.prepare(code.replace("-s", ""))
        args = {
            "discord": discord,
            "commands": commands,
            "sys": sys,
            "os": os,
            "requests": requests,
            "imp": __import__,
            "self": self,
            "ctx": ctx,

        }

        try:
            exec(f"async def func():{code}", args)
            a = time()

            response = await eval("func()", args)
            if silent or (response is None) or isinstance(response, discord.Message):
                del args, code
                return

            await ctx.send(
                f"```py\n{self.resolve_variable(response)}````{type(response).__name__} | {(time() - a) / 1000} ms`")
        except Exception as e:
            await ctx.send(f"Error occurred:```\n{type(e).__name__}: {str(e)}```")

        del args, code, silent

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, module: str):
        """Reloads a module."""
        if module == "all":
            i = 0
            j = 0
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    try:
                        self.bot.unload_extension(f'cogs.{filename[:-3]}')
                        self.bot.load_extension(f'cogs.{filename[:-3]}')
                        i += 1
                    except Exception as e:
                        print('{}: {}'.format(type(e).__name__, e))
                        await ctx.send('{}: {}'.format(type(e).__name__, e))
                    j += 1
            print(f'**{i}/{j}** extensions have been reloaded.')
            await ctx.send(f'**{i}/{j}** extensions have been reloaded.')
            return

        try:
            self.bot.unload_extension(f"cogs.{module}")
            self.bot.load_extension(f"cogs.{module}")
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            print(f'Extension {f"cogs.{module}"} has been reloaded.')
            await ctx.send(f'Extension {f"cogs.{module}"} has been reloaded.')

    @_reload.error
    async def _reload_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing the module argument.")

def setup(bot):
    bot.add_cog(Admin(bot))
