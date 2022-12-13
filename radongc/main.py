import discord
from discord.ext import commands
import os
intents = discord.Intents()
intents.members=True
intents.guilds=True
intents.typing=True
intents.voice_states=True
intents.messages = True
intents.bans = True
intents.dm_messages = True
intents.reactions = True
import logging
a = []
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s'))
logger.addHandler(handler)
logger.info(logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s'))

client = commands.AutoShardedBot(command_prefix=",", case_insensitive=True, intents=intents)
client.remove_command("help")
x = 1
for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):

            client.load_extension(f"cogs.{filename[:-3]}")
            print(f"[COGS] ~> {x}. parancsfájl betöltve\n ")
            x = x +1

@client.event
async def on_ready():
    for x in client.commands:
        a.append(x)
    print(f"Radon GlobalChat elindult!")
    print(f"====================================================================")
    
client.run("NzEzMDE0NjAyODkxMjY0MDUx.XsZ8mA.UDSc2dTj_dmsZWj3Ul1vb3_32_I")
