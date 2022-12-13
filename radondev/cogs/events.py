import asyncio
import discord
from discord.ext import commands
from main import db
import datetime
import random

time_window_milliseconds = 1500
max_msg_per_window = 5
author_msg_times = {}

async def xpgen():
            a = random.randint(1, 3)
            return a

async def level_up(user, message, guild):
            cursor = db.cursor()
            cursor.execute("SELECT level, xp FROM levels WHERE user_id={} AND guild_id={}".format(message.author.id, message.guild.id))
            a = cursor.fetchall()
            lvl_start = a[0][0]
            experience=a[0][1]
            lvl_end = int(experience ** (1 / 4))
            if lvl_start < lvl_end:
                cursor.execute("UPDATE levels SET level={} WHERE user_id={} AND guild_id={}".format(lvl_end, message.author.id, message.guild.id))
                db.commit()
                asd = await message.channel.send(f'{user.mention} szintet léptél! Jelenlegi szinted: {lvl_end}')
                await asyncio.sleep(5)
                await asd.delete()
            else:
                db.commit() 

def get_prefix(client, ctx):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM `prefix` WHERE server_id={int(ctx.guild.id)}")
    result = cursor.fetchall()
    if len(result) == 0:
        default_prefix = ","
        cursor = db.cursor()
        cursor.execute("INSERT INTO prefix (server_id, prefix) VALUES (%s, %s)", (int(ctx.guild.id), default_prefix))
        db.commit()
        return default_prefix
    else:
        return result[0][1]


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

#    @commands.Cog.listener()
#    async def on_member_join(self, member):
#        cursor = db.cursor()
#        cursor.execute(f"SELECT * FROM autorole WHERE guild_id={member.guild.id}")
#        result = cursor.fetchall()
#        if not len(result) == 0:
#            role = discord.utils.get(member.guild.roles, id=result[0][1])
#            await member.add_roles(role)
#        else:
#            pass
#        cursor.execute(f"SELECT * FROM welcomeJoin WHERE guild_id={member.guild.id}")
#        result = cursor.fetchall()
#        if len(result) == 0:
#            pass
#        else: 
#            channel = self.client.get_channel(result[0][1])
#            embed = discord.Embed(title="<:radon_plusz:811191514361102376> Új tag!", description=f"{member.mention} becsatlakozott a szerverre!\nVele együtt ennyien vagyunk: **{len(member.guild.members)}**!", color=0x03fc2c)
#            embed.set_thumbnail(url=member.avatar_url)
#            await channel.send(embed=embed)

    @commands.command(usage=",level <be/ki>")
    async def level(self, ctx, option):
        if ctx.author.guild_permissions.administrator:
            if option == "ki" or option == "off":
                cursor = db.cursor()
                cursor.execute("SELECT * FROM levelSetting WHERE guild_id={}".format(ctx.guild.id))
                result = cursor.fetchall()
                if len(result) == 0:
                    await ctx.send("A level rendszer már ki van kapcsolva!")
                else:
                    cursor.execute("DELETE FROM levelSetting WHERE guild_id={}".format(ctx.guild.id))
                    db.commit()
                    await ctx.send("A level rendszer kikapcsolásra került!")
            elif option == "be" or option == "on":
                cursor = db.cursor()
                cursor.execute("SELECT * FROM levelSetting WHERE guild_id={}".format(ctx.guild.id))
                result = cursor.fetchall()
                if not len(result) == 0:
                    await ctx.send("A level rendszer már be van kapcsolva!")
                else:
                    cursor.execute("INSERT INTO levelSetting (guild_id, valasz) VALUES ({}, 1)".format(ctx.guild.id))
                    db.commit()
                    await ctx.send("A level rendszer bekapcsolásra került!")
            else:
                await ctx.send("Nincs ilyen választási lehetőség! (be, ki, on, off)")
        else:
            perm = "Adminisztrátor"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
            return

    @commands.command()
    async def rank(self, ctx):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM levelSetting WHERE guild_id={} AND valasz=1".format(ctx.guild.id))
        result0 = cursor.fetchall()
        if not len(result0) == 0:
            cursor.execute("SELECT xp, level FROM levels WHERE user_id={} AND guild_id={}".format(ctx.author.id, ctx.guild.id))
            a = cursor.fetchall()
            b = a[0][0]
            c = a[0][1]
            db.commit()
            moneyEmbed = discord.Embed(title="Szint", color=0xFF9900, timestamp=datetime.datetime.utcnow())
            moneyEmbed.add_field(name="Szinted", value=c, inline=False)
            moneyEmbed.add_field(name="XP-d", value=b,  inline=False)
            moneyEmbed.set_footer(text="Radon × Szintrendszer")
            moneyEmbed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.reply(embed=moneyEmbed, mention_author=False)
            
        else:
            await ctx.send("A level rendszer ki van kapcsolva ezen a szerveren!")

    @commands.command(usage=",chignore <add/remove> <#csatorna>")
    async def chignore(self, ctx, option, channel: discord.TextChannel):
        if ctx.author.guild_permissions.manage_channels:
            cursor = db.cursor(buffered=True)
            cursor.execute("SELECT * FROM levelSetting WHERE guild_id={} AND valasz=1".format(ctx.guild.id))
            result0 = cursor.fetchall()
            if not len(result0) == 0:
                if option == "add":
                    
                    cursor.execute(f"SELECT * FROM ignored WHERE guild_id={ctx.guild.id} AND ignoredChLevel={channel.id}")
                    result = cursor.fetchall()
                    if (len(result)==0):
                        cursor.execute("INSERT INTO ignored (ignoredChLevel, guild_id) VALUES ({}, {})".format(ctx.guild.id, channel.id))
                        db.commit()
                        await ctx.reply(f"Sikeresen rögzítettem a csatornát ({channel.mention}) a tiltott csatornákra. Mostantól itt nem lehet XP-t szerezni.")
                    else:
                        await ctx.reply("Ezt a csatorna tiltólistán van már!")
                        db.commit()
                elif option == "remove":
                    cursor.execute("SELECT * FROM ignored WHERE guild_id={} AND ignoredChLevel={}".format(ctx.guild.id, channel.id))
                    result = cursor.fetchall()
                    if (len(result)==0):
                        await ctx.reply("Ezt a csatorna nincs tiltólistán!")
                        db.commit()
                    else:
                        cursor.execute("DELETE FROM ignored WHERE ignoredChLevel={}".format(channel.id))
                        db.commit()
                        await ctx.reply(f"Sikeresen töröltem a csatornát ({channel.mention}) a tiltott csatornákról. Mostantól itt lehet XP-t szerezni.")
                else:
                    await ctx.send(f"Nincs ilyen választási lehetőség! (add, remove)")
            else:
                await ctx.reply("A szint rendszer ki van kapcsolva ezen a szerveren! (,level be)")
        else:
            perm = "Üzenetek kezelése"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
            return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM welcomeLeave WHERE guild_id={member.guild.id}")
        result = cursor.fetchall()
        if len(result) == 0:
            pass
        else:
            channel = self.client.get_channel(result[0][1])
            embed = discord.Embed(title="<:radon_minusz:811191514527957003> Kilépés!", description=f"`{member}` kilépett a szerverről!\nMár csak ennyien maradtunk: **{len(member.guild.members)}**!", color=0xfc0303)
            embed.set_thumbnail(url=member.avatar_url)
            await channel.send(embed=embed)

#    @commands.Cog.listener()
#    async def on_message(self, message):
#        if message.author.id == 495263201768767494 or message.author.id == 696708705688748192:
#            return
#        if self.client.user.mentioned_in(message):
#            if message.reference is not None:
#                return
#            if "@everyone" in message.content.lower() or "@here" in message.content.lower():
#                return
#            #if ctx.reply:
#                #return
#            embed = discord.Embed(description=f"<:radon_plusz:811191514361102376> Üdv!\nÉn Radon vagyok, egy fejlett magyar Discord bot.\nPrefixem: `,`\n[**Support szerverünk**](https://discord.gg/McmvAkstTV)\n[**Weboldalunk**](https://radonbot.hu/)", color = 0xe9b703)
#            await message.reply(embed=embed, mention_author=False)
#        elif not message.author.bot:
#            cursor = db.cursor(buffered=True)
#            cursor.execute("SELECT * FROM levelSetting WHERE guild_id={} AND valasz=1".format(message.guild.id))
#            result0 = cursor.fetchall()
#            if not len(result0) == 0:
#                cursor.execute("SELECT * FROM ignored WHERE ignoredChLevel={} AND guild_id={}".format(message.channel.id, message.guild.id))
#                result1 = cursor.fetchall()
#                if len(result1) == 0:
#                    a = await xpgen()
#                    cursor.execute("SELECT * FROM levels WHERE user_id={} AND guild_id={}".format(message.author.id, message.guild.id))
#                    result = cursor.fetchall()
#                    if (len(result) == 0):
#                        cursor.execute("INSERT INTO levels (guild_id, user_id, level, xp) values ({}, {}, 0, {})".format(message.guild.id, message.author.id, a))
#                        db.commit()
#                    else:
#                        newXP=result[0][3] + a
#                        cursor.execute("UPDATE `levels` SET xp={} WHERE user_id={} AND guild_id={}".format(int(newXP), int(message.author.id), int(message.guild.id)))
#                        cursor.execute(f"UPDATE `levels` SET user_avatar='{message.author.avatar_url}' WHERE user_id={int(message.author.id)} AND guild_id={int(message.guild.id)}")
#                        cursor.execute("UPDATE `levels` SET user_name='{}' WHERE user_id={} AND guild_id={}".format(str(message.author.name), int(message.author.id), int(message.guild.id)))
#                        cursor.execute("UPDATE `levels` SET user_discrim='{}' WHERE user_id={} AND guild_id={}".format(int(message.author.discriminator), int(message.author.id), int(message.guild.id)))
#                        db.commit()
#                        await level_up(user=message.author, message=message, guild=message.guild)
#                else:
#                    db.commit()
#            else:
#                pass
#            #Anti HTTPS
#            cursor.execute(f"SELECT * FROM bypassAutoMod WHERE guild_id={message.guild.id} AND user_id={message.author.id}")
#            result = cursor.fetchall()
#            if len(result) == 0:
#                if "https" in message.content.lower():
#                    cursor.execute(f"SELECT * FROM antilink WHERE guild_id={message.guild.id}")
#                    result = cursor.fetchall()
#                    if not len(result) == 0:
#                        await message.delete()
#                        await message.channel.send(f"{message.author}, neked nincs jogod linkeket küldeni!")
#                    else: pass
#                #ANTI INVITE
#                if "discord.gg/invite" in message.content.lower():
#                    cursor.execute(f"SELECT * FROM antiinvite WHERE guild_id={message.guild.id}")
#                    result = cursor.fetchall()
#                    if not len(result) == 0:
#                        await message.delete()
#                        await message.channel.send(f"{message.author}, neked nincs jogod inviteokat küldeni!")
#                if "discord.com/invite" in message.content.lower():
#                    cursor.execute(f"SELECT * FROM antiinvite WHERE guild_id={message.guild.id}")
#                    result = cursor.fetchall()
#                    if not len(result) == 0:
#                        await message.delete()
#                        await message.channel.send(f"{message.author}, neked nincs jogod inviteokat küldeni!")
#                    else: pass
#                if "discord.gg/" in message.content.lower():
#                    cursor.execute(f"SELECT * FROM antiinvite WHERE guild_id={message.guild.id}")
#                    result = cursor.fetchall()
#                    if not len(result) == 0:
#                        await message.delete()
#                        await message.channel.send(f"{message.author}, neked nincs jogod inviteokat küldeni!")
#                if "discord.com/" in message.content.lower():
#                    cursor.execute(f"SELECT * FROM antiinvite WHERE guild_id={message.guild.id}")
#                    result = cursor.fetchall()
#                    if not len(result) == 0:
#                        await message.delete()
#                        await message.channel.send(f"{message.author}, neked nincs jogod inviteokat küldeni!")
#                #ANTI HTTP  
#                if "http" in message.content.lower():
#                    cursor.execute(f"SELECT * FROM antilink WHERE guild_id={message.guild.id}")
#                    result = cursor.fetchall()
#                    if not len(result) == 0:
#                        await message.delete()
#                        await message.channel.send(f"{message.author}, neked nincs jogod linkeket küldeni!")
#                    else: pass
#                """swears = [ "teszt" ]
#                if swears in message.content.lower():
#                    cursor.execute(f"SELECT *FROM antiswear WHERE guild_id={message.guild.id}")
#                    result = cursor.fetchall()
#                    if not len(result) == 0:
#                        await message.delete()
#                        await message.channel.send(f"{message.author}, ne káromkodj!")
#                    else: pass"""
#                cursor.execute(f"SELECT * FROM antispam WHERE guild_id={message.guild.id}")
#                result = cursor.fetchall()
#                if not len(result) == 0:
#                    global author_msg_counts
#                    author_id = message.author.id
#                    # Get current epoch time in milliseconds
#                    curr_time = datetime.datetime.now().timestamp() * 1000
#                    # Make empty list for author id, if it does not exist
#                    if not author_msg_times.get(author_id, False):
#                        author_msg_times[author_id] = []
#                    # Append the time of this message to the users list of message times
#                    author_msg_times[author_id].append(curr_time)
#                    # Find the beginning of our time window.
#                    expr_time = curr_time - time_window_milliseconds
#                    # Find message times which occurred before the start of our window
#                    expired_msgs = [
#                        msg_time for msg_time in author_msg_times[author_id]
#                        if msg_time < expr_time
#                    ]
#                    # Remove all the expired messages times from our list
#                    for msg_time in expired_msgs:
#                        author_msg_times[author_id].remove(msg_time)
#                    # ^ note: we probably need to use a mutex here. Multiple threads
#                    # might be trying to update this at the same time. Not sure though.
#                    if len(author_msg_times[author_id]) > max_msg_per_window:
#                        await message.delete()
#                        asd = await message.channel.send(f"{str(message.author)} kérlek ne spamelj!")
#                        await asyncio.sleep(2)
#                        await asd.delete()
#                else:
#                    pass
#            else:
#                pass
#        #await self.client.process_commands(message)

#    @commands.Cog.listener()
#    async def on_guild_join(self, guild):
#        channel = self.client.get_channel(855526480267313212)
#        await channel.send(f"Uj szerver\nNev: {guild.name}\nTagok: {len(guild.members)}\nTulaj: {guild.owner}\nTulaj ID: no intents")
#
#    @commands.Cog.listener()
#    async def on_guild_remove(self, guild):
#        channel = self.client.get_channel(855526480267313212)
#        await channel.send(f"kirugtak egy szerverrol\nNev: {guild.name}\nTagok: {len(guild.members)}\nTulaj: {guild.owner}\nTulaj ID: no intents")

def setup(client):
    client.add_cog(Events(client))
