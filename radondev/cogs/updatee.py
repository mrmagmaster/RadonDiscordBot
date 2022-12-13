import discord
from discord.ext import commands
import datetime
import asyncio
import json
import random

class Update(commands.Cog):
    def __init__(self, client):
        self.client = client



def setup(client):
    client.add_cog(Update(client))
