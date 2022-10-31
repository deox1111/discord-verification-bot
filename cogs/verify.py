import time
import discord
import psutil
import os
import requests
import aiohttp
import random
import json


from discord.ext import commands
from discord.utils import get
from utils import default, http



class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()
        self.process = psutil.Process(os.getpid())
    
    @commands.command()
    async def verify(self, ctx, *, code: str):

        await ctx.message.delete()
        key = self.config['api_code']
        r = requests.get(f"https://deox.space/panel/api?verifyCode={code}&discordID={ctx.author.id}&key={key}")
        verify = r.json()
        fields = [
            {'name': 'verified?', 'value': verify['verified']}
        ]

        for field in fields:
            if field['value'] == 'yes': 
                member = ctx.message.author
                role = get(member.guild.roles, name="verified")
                await member.add_roles(role)

         
            else:
                return


        

async def setup(bot):
    await bot.add_cog(Verification(bot))
