from discord.ext import commands
from aiohttp import ClientSession, ClientConnectorError
from core.embeds import *
import re
import json
import random

GET_KEYS = ["-h"]
POST_KEYS = ["-h", "-d"]

class Requests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = None  # Initialize session once and never again

    async def init_session(self):
        self.session = await ClientSession().__aenter__()
        print("Session initialized")

    async def _request(self, url, method, **kwargs):
        async with getattr(self.session, method)(url, **kwargs) as resp:
            try:
                return await resp.text()
            except UnicodeDecodeError:
                return await resp.read()

    def _get_params(self, text):
        w = ""
        ww = ""
        wd = False
        wt = False
        rd = {}
        for a in text.split():
            p = True
            if not a.startswith('-'):
                wt = True
            else:
                wt = False
            if a.startswith('-'):
                w = a
                if wt is True:
                    p = False
                else:
                    p = True
                wt = False
            if not p:
                if not w == ww:
                    wd = False
                    ww = w
                else:
                    wd = True
            if not w == "":
                if wt:
                    try:
                        rd[w] += a + ' '
                    except Exception:
                        rd[w] = a + ' '

        for i in rd:
            if rd[i][-1] == " ":
                rd[i] = rd[i][:-1]
        return rd

    def validate_url(self, url):
        validate = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return re.match(validate, url) is not None

    def validate_dict(self, data):
        try:
            json_data = json.loads("{" + data + "}")
            return json_data
        except Exception as e:
            return e

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def get(self, ctx, url, *, args=None):
        valid_url = self.validate_url(url)

        if not valid_url:
            embed = InvalidURLEmbed(url)
            await ctx.send(embed=embed)
            return

        kwargs = {}

        if args:
            params = self._get_params(args)

            for k in params:
                if k not in GET_KEYS:
                    embed = UnexpectedKeyEmbed(k, 'GET')
                    await ctx.send(embed=embed)
                    return

            if '-h' in params:
                valid_headers = self.validate_dict(params['-h'])
                if isinstance(valid_headers, Exception):
                    embed = InvalidHeadersEmbed(valid_headers)
                    await ctx.send(embed=embed)
                    return
                kwargs['headers'] = valid_headers

            if '-d' in params:
                embed = UnexpectedKeyEmbed('-d', 'GET')
                await ctx.send(embed=embed)
                return

        try:
            resp = await self._request(url, 'get', **kwargs)

            if isinstance(resp, bytes):
                embed = ResponseEmbed("Received bytes")
                embed.set_image(url=url)
            else:
                embed = ResponseEmbed(resp)
            await ctx.send(embed=embed)
        except ClientConnectorError:
            embed = IncorrectURL(url)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def post(self, ctx, url, *, args=None):
        valid_url = self.validate_url(url)

        if not valid_url:
            embed = InvalidURLEmbed(url)
            await ctx.send(embed=embed)
            return

        kwargs = {}

        if args:
            params = self._get_params(args)

            for k in params:
                if k not in POST_KEYS:
                    embed = UnexpectedKeyEmbed(k, 'POST')
                    await ctx.send(embed=embed)
                    return

            if '-h' in params:
                valid_headers = self.validate_dict(params['-h'])
                if isinstance(valid_headers, Exception):
                    embed = InvalidHeadersEmbed(valid_headers)
                    await ctx.send(embed=embed)
                    return
                kwargs['headers'] = valid_headers

            if '-d' in params:
                valid_data = self.validate_dict(params['-d'])
                if isinstance(valid_data, Exception):
                    embed = InvalidDataEmbed(valid_data)
                    await ctx.send(embed=embed)
                    return
                kwargs['data'] = valid_data

        try:
            resp = await self._request(url, 'post', **kwargs)

            if isinstance(resp, bytes):
                embed = ResponseEmbed("Received bytes")
                embed.set_image(url=url)
            else:
                embed = ResponseEmbed(resp)
            await ctx.send(embed=embed)
        except ClientConnectorError:
            embed = IncorrectURL(url)
            await ctx.send(embed=embed)


    @get.error
    async def get_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(random.choice(["Whoa whoa, you gotta wait 2 seconds before making another get request.", "What's the hurry? Wait 2 seconds before making another get request.", "You can't just spam like that, you gotta wait 2 seconds before making another get request."]))
            return
        raise error

    @post.error
    async def post_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(random.choice(["Whoa whoa, you gotta wait 2 seconds before making another post request.", "What's the hurry? Wait 2 seconds before making another post request.", "You can't just spam like that, you gotta wait 2 seconds before making another post request."]))
            return
        raise error

def setup(bot):
    bot.add_cog(Requests(bot))
