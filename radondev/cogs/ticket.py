import discord
from discord.ext import commands
import datetime
import random
import asyncio
import json

class Ticket(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 30, type=commands.BucketType.user)
    async def ticket(self, ctx):
        with open("data.json") as f:
            data = json.load(f)
        ticket_number = int(data["ticket-counter"])
        ticket_number += 1
        ticket_channel = await ctx.guild.create_text_channel(f"ticket-{ctx.author}")
        await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)
        for role_id in data["valid-roles"]:
            role = ctx.guild.get_role(role_id)
            await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
        await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
        em = discord.Embed(title="Sikeresen elkészült a ticketed: {}#{}".format(ctx.author.name, ctx.author.discriminator), timestamp=datetime.datetime.utcnow(), color=0xFF9900)
        await ticket_channel.send(embed=em)
        pinged_msg_content = ""
        non_mentionable_roles = []
        if data["pinged-roles"] != []:
            for role_id in data["pinged-roles"]:
                role = ctx.guild.get_role(role_id)
                pinged_msg_content += role.mention
                pinged_msg_content += " "
                if role.mentionable:
                    pass
                else:
                    await role.edit(mentionable=True)
                    non_mentionable_roles.append(role)
            await ticket_channel.send(pinged_msg_content)
            for role in non_mentionable_roles:
                await role.edit(mentionable=False)
        data["ticket-channel-ids"].append(ticket_channel.id)
        data["ticket-counter"] = int(ticket_number)
        with open("data.json", 'w') as f:
            json.dump(data, f)
        created_em = discord.Embed(description="Sikeres létrehozás ({})".format(ticket_channel.mention), timestamp=datetime.datetime.utcnow(), color=0xFF9900)
        created_em.set_author(name=f"Ticket × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=created_em)

    @commands.command()
    async def close(self, ctx):
        with open('data.json') as f:
            data = json.load(f)
        if ctx.channel.id in data["ticket-channel-ids"]:
            channel_id = ctx.channel.id
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "igen"
            try:
                em = discord.Embed(description="Biztos lezárod a ticketet? Ha igen, írd be a következőt: `igen`", color=0xFF9900, timestamp=datetime.datetime.utcnow())
                em.set_author(name=f"Ticket × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=em)
                await self.client.wait_for('message', check=check, timeout=30)
                await ctx.channel.delete()
                index = data["ticket-channel-ids"].index(channel_id)
                del data["ticket-channel-ids"][index]
                with open('data.json', 'w') as f:
                    json.dump(data, f)
            except asyncio.TimeoutError:
                em = discord.Embed(description="Hiba történt! Kérlek írd be újra a parancsot.", color=0xFF9900, timestamp=datetime.datetime.utcnow())
                em.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=em)

def setup(client):
    client.add_cog(Ticket(client))
