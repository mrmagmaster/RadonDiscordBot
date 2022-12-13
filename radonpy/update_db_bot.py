import discord
from discord.ext import commands
import asyncio
import mysql.connector as myc



dbconfig = {
    "host": "localhost",
    "user": "root",
    "passwd": "cD5WYBuGTp",
    "db": "db",
    "auth_plugin": "mysql_native_password"
}

db = myc.connect(**dbconfig,
                pool_name="radon2",
                pool_size=16)


bot = commands.Bot(command_prefix="jfkvrjkgasjkhfjh")
bot.remove_command("help")
@bot.event
async def on_ready():
    print("ready")
    await db_update()

async def db_update():
    while True:
        a = 0
        for guild in bot.guilds:
            a = a + guild.member_count
        cursor = db.cursor()
        cursor.execute("SELECT * FROM data")
        cursor.fetchall()
        cursor.execute(f"UPDATE data SET servers={len(bot.guilds)}, members={a}, channels={len(set(bot.get_all_channels()))}")
        db.commit()
        await asyncio.sleep(3600)
        

bot.run("NzEzMDE0NjAyODkxMjY0MDUx.XsZ8mA.UDSc2dTj_dmsZWj3Ul1vb3_32_I")
