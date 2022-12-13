from discord.ext import commands
import datetime
import discord
import asyncio
import os
import random
import discord_webhook
from main import db

szin = 0xFF9900

class Log(commands.Cog):
    def __init__(self, client):
        self.client = client
#    @commands.command(usage=",setlog [#csatorna]", aliases=["log", "addlog", "logbe", "logset", "enablelog"])
#    async def setlog(self, ctx, channel: discord.TextChannel):
#        if not ctx.author.id == 406137394228625419: return
#        try:
#            if ctx.author.guild_permissions.administrator:
#                    cursor = db.cursor()
#                    cursor.execute(f"SELECT * FROM `log` WHERE guild_id={ctx.guild.id}")
#                    result = cursor.fetchall()
#                    if len(result) == 0:
#                        with open('radon.png', 'rb') as f:
#                            avatar = f.read()
#                        webhook = await channel.create_webhook(name="Radon", avatar=avatar)
#                        wb = str(webhook.url).split('/', 5)
#                        print(wb[5])
#                        print(channel.id)
#                        print(ctx.guild.id)
#                        cursor.execute(f"INSERT INTO `log` (guild_id, channel_id, webhook) VALUES ('{ctx.guild.id}', '{channel.id}', '{wb[5]}')")
#                        db.commit()
#                        await ctx.reply(content=f"<:radon_pipa:811191514369753149> A log sikeresen beállítva a {channel.mention} csatornára!", mention_author=False)
#                    else:
#                        await ctx.reply(content=f"<:radon_x:811191514482212874> Ezen a szerveren már be van kapcsolva a log rendszer!", mention_author=False)
#            else:
#                await ctx.reply(content="<:radon_x:811191514482212874> Nincs jogod a parancs használathához, szükséges jog: `Adminisztrátor`", mention_author=False)
#        except:
#            raise
#
#    @commands.command(aliases=["rmlog", "removelog", "logki", "logreset", "disablelog", "remlog"], usage=",removelog [#csatorna]")
#    async def dellog(self, ctx):
#        if ctx.author.guild_permissions.administrator:
#            cursor = db.cursor()
#            cursor.execute(f"SELECT * FROM `log` WHERE guild_id={int(ctx.guild.id)}")
#            result = cursor.fetchall()
#            if len(result)==0:
#                await ctx.reply(content="<:radon_x:811191514482212874> A szerveren nincs bekapcsolva a log rendszer!", mention_author=False)
#                return
#            else:
#                cursor.execute(f"DELETE FROM `log` WHERE guild_id={int(ctx.guild.id)}")
#                db.commit()
#                await ctx.reply(content=f"<:radon_pipa:811191514369753149> A log sikeresen kikapcsolva!", mention_author=False)
#        else:
#            await ctx.reply(content="<:radon_x:811191514482212874> Nincs jogod a parancs használathához, szükséges jog: `Adminisztrátor`", mention_author=False)
#
#    @commands.Cog.listener()
#    async def on_message_delete(self, ctx):
#        cursor = db.cursor()
#        cursor.execute(f"SELECT * FROM `log` WHERE guild_id={int(ctx.guild.id)}")
#        result = cursor.fetchall()
#        if len(result) == 0:
#            return
#        else:
#            if ctx.author.bot: return
#            if not result[0][0] == ctx.guild.id: return 
#            cleanmsg = ctx.content
#            
#            embed = discord_webhook.DiscordEmbed(title="Üzenet törlése", description=f"Egy üzenetet töröltek {ctx.author.mention} (**{ctx.author}**) által a {ctx.channel.mention} csatornában.", color=0xFF9900)
#            embed.add_embed_field(name="Üzenet", value=cleanmsg)
#            webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#            webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#            webhook.add_embed(embed)
#            webhook.execute()
#
#    @commands.Cog.listener()
#    async def on_member_join(self, ctx):
#        cursor = db.cursor()
#        cursor.execute(f"SELECT * FROM `log` WHERE guild_id={int(ctx.guild.id)}")
#        result = cursor.fetchall()
#        if len(result) == 0:
#            return
#        else:
#            if ctx.author.bot: return
#            if not result[0][0] == ctx.guild.id: return 
#            embed = discord_webhook.DiscordEmbed(title="Csatlakozás", description=f"{ctx.author.mention} (**{ctx.author}**) csatlakozott a szerverhez. Jelenlegi létszám: {len(ctx.guild.members)}", color=0xFF9900)
#            webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#            webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#            webhook.add_embed(embed)
#            webhook.execute()
#
#    @commands.Cog.listener()
#    async def on_member_remove(self, ctx):
#        cursor = db.cursor()
#        cursor.execute(f"SELECT * FROM `log` WHERE guild_id={int(ctx.guild.id)}")
#        result = cursor.fetchall()
#        if len(result) == 0:
#            return
#        else:
#            if ctx.author.bot: return
#            if not result[0][0] == ctx.guild.id: return 
#            embed = discord_webhook.DiscordEmbed(title="Kilépés", description=f"{ctx.author.mention} (**{ctx.author}**) kilépett a szerverről. Jelenlegi létszám: {len(ctx.guild.members)}", color=0xFF9900)
#            webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#            webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#            webhook.add_embed(embed)
#            webhook.execute()
#
#    @commands.Cog.listener()
#    async def on_channel_update(self, before, after):
#        cursor = db.cursor()
#        cursor.execute(f"SELECT * FROM `log` WHERE guild_id={int(before.guild.id)}")
#        result = cursor.fetchall()
#        if len(result) == 0:
#            return
#        else:
#            if ctx.author.bot: return
#            if not result[0][0] == before.guild.id: return 
#            if before.type == discord.ChannelType.voice:
#                embed = discord_webhook.DiscordEmbed(title="Hangcsatorna módosítása", description=f"{after.mention} módosítva!", color=szin)
#                if before.region != after.region:
#                    if before.region == "europe": before.region = "Európa"
#                    elif before.region == "usa": before.region = "Amerika"
#                    elif before.region == "brasil": before.region = "Brazília"
#                    elif before.region in ("hong-kong", "hong_kong", "hong kong"): before.region = "Hong Kong"
#                    elif before.region == "india": before.region = "India"
#                    elif before.region == "japan": before.region = "Japán"
#                    elif before.region == "russia": before.region = "Oroszország"
#                    elif before.region == "singapore": before.region = "Szingapúr"
#                    elif before.region in ("south-africa", "south_africa", "south africa"): before.region = "Dél-Afrika"
#                    elif before.region == "sydney": before.region = "Sydney"
#                    elif before.region in ("us-central", "us-cen", "us_central", "us_cen", "us central", "us cen"): before.region = "Közép-Amerika"
#                    elif before.region in ("us-east", "us_east", "us east"): before.region = "Kelet-Amerika"
#                    elif before.region in ("us-south", "us_south", "us south"): before.region = "Dél-Amerika"
#                    elif before.region in ("us-west", "us_west", "us west"): before.region = "Észak-Amerika"
#                    else: before.region = "Nem érzékelhető vagy prémium régió"
#                    if after.region == "europe": after.region = "Európa"
#                    elif after.region == "usa": after.region = "Amerika"
#                    elif after.region == "brasil": after.region = "Brazília"
#                    elif after.region in ("hong-kong", "hong_kong", "hong kong"): after.region = "Hong Kong"
#                    elif after.region == "india": after.region = "India"
#                    elif after.region == "japan": after.region = "Japán"
#                    elif after.region == "russia": after.region = "Oroszország"
#                    elif after.region == "singapore": after.region = "Szingapúr"
#                    elif after.region in ("south-africa", "south_africa", "south africa"): after.region = "Dél-Afrika"
#                    elif after.region == "sydney": after.region = "Sydney"
#                    elif after.region in ("us-central", "us-cen", "us_central", "us_cen", "us central", "us cen"): after.region = "Közép-Amerika"
#                    elif after.region in ("us-east", "us_east", "us east"): after.region = "Kelet-Amerika"
#                    elif after.region in ("us-south", "us_south", "us south"): after.region = "Dél-Amerika"
#                    elif after.region in ("us-west", "us_west", "us west"): after.region = "Észak-Amerika"
#                    else: after.region = "Nem érzékelhető vagy prémium régió"
#                    embed.add_embed_field(name="Régi régió", value=before.region)
#                    embed.add_embed_field(name="Új régió", value=after.region)
#                if before.name != after.name:
#                    embed.add_embed_field(name="Régi név", value=before, inline=True)
#                    embed.add_embed_field(name="Új név", value=after, inline=True)
#                if before.bitrate != after.bitrate:
#                    embed.add_embed_field(name="\u200b", value="\u200b")
#                    embed.add_embed_field(name="Régi bitráta", value=f"**{before.bitrate}**kbps", inline=True)
#                    embed.add_embed_field(name="Új bitráta", value=f"**{after.bitrate}**kbps", inline=True)
#                webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#                webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#                webhook.add_embed(embed)
#                webhook.execute()
#            if before.type == discord.ChannelType.text:
#                embed = discord_webhook.DiscordEmbed(title="Szöveges csatorna módosítása", description=f"{after.mention} módosítva!", color=szin)
#                if before.name != after.name:
#                    embed.add_embed_field(name="Régi név", value=before, inline=True)
#                    embed.add_embed_field(name="Új név", value=after, inline=True)
#                if before.topic != after.topic:
#                    embed.add_embed_field(name="\u200b", value="\u200b")
#                    embed.add_embed_field(name="Régi téma (topic)", value=before.topic,inline=True)
#                    embed.add_embed_field(name="Új téma", value=after.topic,inline=True)
#                webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#                webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#                webhook.add_embed(embed)
#                webhook.execute()
#
#    @commands.Cog.listener()
#    async def on_message_edit(self, before, after):
#        cursor = db.cursor()
#        cursor.execute(f"SELECT * FROM `log` WHERE guild_id={int(before.guild.id)}")
#        result = cursor.fetchall()
#        if len(result) == 0:
#            return
#        else:
#            if before.author.bot: return
#            if not result[0][1] == before.channel.id: return  
#            if before.content != after.content:
#                embed = discord_webhook.DiscordEmbed(title="Üzenet szerkesztése", description=f"A(z) {after.channel.mention} csatornában üzenetet szerkesztett {after.author.mention} (**{after.author}**)!", color=szin)
#                embed.add_embed_field(name="Régi üzenet", value=before.content,inline=True)
#                embed.add_embed_field(name="Új üzenet", value=after.content,inline=True)
#                webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#                webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#                webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#                webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#                webhook.add_embed(embed)
#                webhook.execute()
#
#    @commands.Cog.listener()
#    async def on_guild_update(self, before, after):
#        cursor = db.cursor()
#        cursor.execute(f"SELECT * FROM `log` WHERE guild_id={int(before.id)}")
#        result = cursor.fetchall()
#        if len(result) == 0:
#            return
#        else:
#            if not result[0][0] == before.id: return
#            if before.name != after.name:
#                embed=discord_webhook.DiscordEmbed(title="Szerver név változtatás", color=szin)
#                embed.add_embed_field(name="Régi név", value=before.name)
#                embed.add_embed_field(name="Új név", value=after.name)
#                webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#                webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#                webhook.add_embed(embed)
#                webhook.execute()
#
#    @commands.Cog.listener()
#    async def on_guild_role_create(self, role):
#        cursor = db.cursor()
#        cursor.execute(f"SELECT * FROM `log` WHERE guild_id={int(role.guild.id)}")
#        result = cursor.fetchall()
#        if len(result) == 0:
#            return
#        else:
#
#            if not result[0][0] == role.guild.id: return 
#            embed=discord_webhook.DiscordEmbed(title="Rang létrehozás", color=szin)
#            embed.add_embed_field(name="Neve", value=role.name)
#            embed.add_embed_field(name="Jogai (számokban)", value=str(role.permissions))
#            webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#            webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#            webhook.add_embed(embed)
#            webhook.execute()
#
#    @commands.Cog.listener()
#    async def on_guild_role_remove(self, role):
#        cursor = db.cursor()
#        cursor.execute(f"SELECT * FROM `log` WHERE guild_id={int(role.guild.id)}")
#        result = cursor.fetchall()
#        if len(result) == 0:
#            return
#        else:
#            if not result[0][0] == ctx.guild.id: return 
#            embed=discord_webhook.DiscordEmbed(title="Rang eltávolítás", color=szin)
#            embed.add_embed_field(name="Neve", value=role.name)
#            embed.add_embed_field(name="Jogai (számokban)", value=str(role.permissions))
#            webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#            webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#            webhook.add_embed(embed)
#            webhook.execute()
#
#    @commands.Cog.listener()
#    async def on_guild_role_update(self, before, after):
#        cursor = db.cursor()
#        cursor.execute(f"SELECT * FROM `log` WHERE guild_id={int(before.guild.id)}")
#        result = cursor.fetchall()
#        if len(result) == 0:
#            return
#        else:
#            if not result[0][0] == before.guild.id: return
#            embed=discord_webhook.DiscordEmbed(title="Rang frissítés", color=szin)
#            if before.name != after.name:
#                embed.add_embed_field(name="Régi neve", value=before.name)
#                embed.add_embed_field(name="Új neve", value=after.name)
#            if before.permissions != after.permissions:
#                embed.add_embed_field(name="Régi jogai (számokban)", value=str(before.permissions))
#                embed.add_embed_field(name="Új jogai (számokban)", value=str(after.permissions))
#            webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#            webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#            webhook.add_embed(embed)
#            webhook.execute()
#
#    @commands.Cog.listener()
#    async def on_guild_emojis_update(self, before, after):
#        if csatorna == 0:
#            return
#        else:
#            if before.guild.id not in allowedservers: return
#            embed=discord_webhook.DiscordEmbed(title="Emoji frissítés (<:{}:{})".format(after.name, after.id), color=szin)
#            embed.add_embed_field(name="Régi név", value=f"{before.name}")
#            embed.add_embed_field(name="Új név", value=f"{after.name}")
#            webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#            webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#            webhook.add_embed(embed)
#            webhook.execute()
#
#    @commands.Cog.listener()
#    async def on_member_ban(self, user):
#        cursor = db.cursor()
#        cursor.execute(f"SELECT * FROM `log` WHERE guild_id={int(user.guild.id)}")
#        result = cursor.fetchall()
#        if len(result) == 0:
#            return
#        else:
#            if not result[0][0] == user.guild.id: return
#            embed=discord_webhook.DiscordEmbed(title="Tag kitiltása", color=szin)
#            embed.add_embed_field(name="Tag neve", value=user)
#            embed.add_embed_field(name="Tag ID-je", value=user.id)
#            embed.set_footer(text="Történt")
#            webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#            webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#            webhook.add_embed(embed)
#            webhook.execute()
#
#    @commands.Cog.listener()
#    async def on_member_unban(self, user):
#        cursor = db.cursor()
#        cursor.execute(f"SELECT * FROM `log` WHERE guild_id={int(user.guild.id)}")
#        result = cursor.fetchall()
#        if len(result) == 0:
#            return
#        else:
#            if not result[0][0] == user.guild.id: return 
#            embed=discord_webhook.DiscordEmbed(title="Tag kitiltásának feloldása", color=szin)
#            embed.add_embed_field(name="Tag neve", value=user)
#            embed.add_embed_field(name="Tag ID-je", value=user.id)
#            embed.set_footer(text="Történt")
#            webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#            webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#            webhook.add_embed(embed)
#            webhook.execute()
#
#    @commands.Cog.listener()
#    async def on_member_kick(self, user):
#        cursor = db.cursor()
#        cursor.execute(f"SELECT * FROM `log` WHERE guild_id={int(user.guild.id)}")
#        result = cursor.fetchall()
#        if len(result) == 0:
#            return
#        else:
#            if not result[0][0] == user.guild.id: return  
#            embed=discord_webhook.DiscordEmbed(title="Tag kirúgása", color=szin)
#            embed.add_embed_field(name="Tag neve", value=user)
#            embed.add_embed_field(name="Tag ID-je", value=user.id)
#            embed.set_footer(text="Történt")
#            webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#            webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#            webhook.add_embed(embed)
#            webhook.execute()
#
#    @commands.Cog.listener()
#    async def on_bulk_message_delete(self, messages):
#        cursor = db.cursor()
#        cursor.execute(f"SELECT * FROM `log` WHERE guild_id={int(messagey.guild.id)}")
#        result = cursor.fetchall()
#        if len(result) == 0:
#            return
#        else:
#            if not result[0][0] == messagey.guild.id: return 
#            xd = " "
#            for i in messages: xd = i + "\n"
#            embed=discord_webhook.DiscordEmbed(title="Tömeges üzenet törlés", description="Üzenetek száma {}\nÜzenetek::\n{}".format(len(messages), xd), color=szin)
#            webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#            webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#            webhook.add_embed(embed)
#            webhook.execute()
#
#    @commands.Cog.listener()
#    async def on_member_update(self, before, after):
#        cursor = db.cursor()
#        cursor.execute(f"SELECT * FROM `log` WHERE guild_id={int(before.guild.id)}")
#        result = cursor.fetchall()
#        if len(result) == 0:
#            return
#        else:
#            if not result[0][0] == before.guild.id: return 
#            if before.status != after.status:
#                embed=discord_webhook.DiscordEmbed(title="Felhasználó státusz módosítás", color=szin)
#                if before.status: embed.add_embed_field(name="Régi státusz", value=before.status)
#                embed.add_embed_field(name="Új státusz", value=after.status)
#                embed.add_embed_field(name="Felhasználó", value=f"{before.author.mention} (**{before.author}**)")
#                webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#                webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#                webhook.add_embed(embed)
#                webhook.execute()
#            if before.activity != after.activity:
#                embed=discord_webhook.DiscordEmbed(title="Felhasználó RPC módosítás", color=szin)
#                if before.activity: embed.add_embed_field(name="Régi RPC", value=before.activity)
#                embed.add_embed_field(name="Új RPC", value=after.activity)
#                embed.add_embed_field(name="Felhasználó", value=f"{before.author.mention} (**{before.author}**)")
#                webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#                webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#                webhook.add_embed(embed)
#                webhook.execute()
#            if before.nickname != after.nickname:
#                embed=discord_webhook.DiscordEmbed(title="Felhasználó becenév változtatás", color=szin)
#                if before.nickname: embed.add_embed_field(name="Régi becenév", value=before.nickname)
#                embed.add_embed_field(name="Új becenév", value=after.nickname)
#                embed.add_embed_field(name="Felhasználó", value=f"{before.author.mention} (**{before.author}**)")
#                webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#                webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#                webhook.add_embed(embed)
#                webhook.execute()
#            if before.roles != after.roles:
#                embed=discord_webhook.DiscordEmbed(title="Felhasználó rang változtatás", color=szin)
#                for i in before.roles: xd=i + ", "
#                if before.roles: embed.add_embed_field(name="Régi rangok", value=xd )
#                for i in after.roles: xd1 = i + ", "
#                embed.add_embed_field(name="Új rangok", value=xd1)
#                embed.add_embed_field(name="Felhasználó", value=f"{before.author.mention} (**{before.author}**)")
#                webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#                webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#                webhook.add_embed(embed)
#                webhook.execute()
#
#    @commands.Cog.listener()
#    async def on_user_update(self, before, after):
#        cursor = db.cursor()
#        cursor.execute(f"SELECT * FROM `log` WHERE guild_id={int(before.guild.id)}")
#        result = cursor.fetchall()
#        if len(result) == 0:
#            return
#        else:
#            if ctx.author.bot: return
#            if not result[0][0] == ctx.guild.id: return 
#            if before.avatar != after.avatar:
#                embed=discord_webhook.DiscordEmbed(title="Felhasználó profilkép frissítés (régi a jobb felső sarokban)", color=szin)
#                embed.add_embed_field(name="Felhasználó", value=f"{before.author.mention} (**{before.author}**)")
#                embed.set_image(url=after.avatar_url)
#                embed.set_thumbnail(url=before.avatar_url)
#                webhook.add_embed(embed)
#                webhook.execute()
#            if before.username != after.username:
#                embed=discord_webhook.DiscordEmbed(title="Felhasználó név frissítés", color=szin)
#                embed.add_embed_field(name="Felhasználó", value=f"{before.author.mention} (**{before.author}**)")
#                embed.add_embed_field(name="Régi név", value=before.username)
#                embed.add_embed_field(name="Új név", value=after.username)
#                webhook.add_embed(embed)
#                webhook.execute()
#            if before.discriminator != after.discriminator:
#                embed=discord_webhook.DiscordEmbed(title="Felhasználó tag frissítés", color=szin)
#                embed.add_embed_field(name="Felhasználó", value=f"{before.author.mention} (**{before.author}**)")
#                embed.add_embed_field(name="Régi tag", value=f"{before.name}**#{before.discriminator}**")
#                embed.add_embed_field(name="Új tag", value=f"{after.name}**#{after.discriminator}**")
#                webhookurl = f"https://discord.com/api/webhooks/{result[0][2]}"
#                webhook = discord_webhook.DiscordWebhook(url=webhookurl, embed=embed)
#                webhook.add_embed(embed)
#                webhook.execute()

def setup(client):
    client.add_cog(Log(client))
