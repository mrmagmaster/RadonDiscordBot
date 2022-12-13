import discord

token = "NzEzMDE0NjAyODkxMjY0MDUx.XsZ8mA.3V5CSO89WmT7d7TIL3lmFdAhpkg"
prefix = "?" # This will be used at the start of commands.

import discord
from discord.ext import commands
from discord.ext.commands import Bot

bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(discord.__version__)
    print('------')

    print('Servers connected to:')
    for guild in bot.guilds:
        print(guild.name)
        


bot.run(token)