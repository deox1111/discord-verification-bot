import time
import discord
import psutil
import os
import requests
import aiohttp
import random

from discord.ext import commands
from utils import default, http



class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()
        self.process = psutil.Process(os.getpid())
    
    @commands.command()
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        message = await ctx.send("pong!")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"WS: {before_ws}ms  |  REST: {int(ping)}ms")

    @commands.command(aliases=["userinfo"])
    async def usercheck(self, ctx, *, username: str):
        """ user info """
        if ctx.author.id in self.config["owners"]:
            
            key = self.config['api_code']
            r = requests.get(f"https://deox.space/panel/api.php?user={username}&key={key}")
            user_lookup = r.json()
            em = discord.Embed(title="user info:", color=random.randrange(0x1000000))
            fields = [
                {'name': 'uid', 'value': user_lookup['uid']},
                {'name': 'username', 'value': user_lookup['username']},
                {'name': 'hwid', 'value': user_lookup['hwid']},
                {'name': 'admin', 'value': user_lookup['admin']},
                {'name': 'sub', 'value': user_lookup['sub']},
                {'name': 'banned', 'value': user_lookup['banned']},
                {'name': 'invited by:', 'value': user_lookup['invitedBy']},
                {'name': 'created at:', 'value': user_lookup['createdAt']},
                {'name': 'verified:', 'value': user_lookup['verified']},
                {'name': 'verify code"', 'value': user_lookup['verifyCode']},
                {'name': 'discord id:', 'value': user_lookup['discordID']},
                {'name': 'last ip:', 'value': user_lookup['lastIP']},
            ]
            for field in fields:
                if field['value']:  
                    em.add_field(name=field['name'], value=field['value'], inline=False)
            return await ctx.send(embed=em)

        await ctx.send(f"no, heck off {ctx.author.name}")



async def setup(bot):
    await bot.add_cog(Information(bot))
