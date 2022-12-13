import discord
from discord.ext import commands
import datetime
import random
import asyncio
import json
global tmsg

class Rticket(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1,120,type=commands.BucketType.user)
    async def ticketsetup(self, ctx, csatorna: discord.TextChannel):
        embed=discord.Embed(title="Ticket", description="Reagálj a :ticket: emojival a ticket létrehozásához!", color=0xff9900)
        embed.set_footer(icon_url=self.client.user.avatar_url, text="Radon × Ticket")
        global msg
        msg = await csatorna.send(embed=embed)
        await msg.add_reaction("🎫")
        def check(m): return m.channel.id==msg.channel.id
        reaction=await self.client.wait_for("reaction", check=check)
        if reaction == "🎫":
            with open("data.json") as f: data = json.load(f)
            ticket_number = int(data["ticket-counter"])
            ticket_number += 1
            ticket_channel = await reaction.guild.create_text_channel(f"ticket-{reaction.author}")
            await ticket_channel.set_permissions(reaction.guild.get_role(reaction.guild.id), send_messages=False, read_messages=False)
            for role_id in data["valid-roles"]:
                role = reaction.guild.get_role(role_id)
                await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
            await ticket_channel.set_permissions(reaction.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
            tmsg=await ticket_channel.send(f"{reaction.author.mention}, a ticketed elkészült! Lezárás a :lock: emojival.")
            await tmsg.add_reaction("🔒")
            pinged_msg_content = ""
            non_mentionable_roles = []
            if data["pinged-roles"] != []:
                for role_id in data["pinged-roles"]:
                    role = reaction.guild.get_role(role_id)
                    pinged_msg_content += role.mention
                    pinged_msg_content += " "
                    if role.mentionable: pass
                else: await role.edit(mentionable=True); non_mentionable_roles.append(role)
                await ticket_channel.send(pinged_msg_content)
                for role in non_mentionable_roles: await role.edit(mentionable=False)
            data["ticket-channel-ids"].append(ticket_channel.id)
            data["ticket-counter"] = int(ticket_number)
            with open("data.json", 'w') as f: json.dump(data, f)
            created_em = discord.Embed(description="Sikeres létrehozás ({})".format(ticket_channel.mention), timestamp=datetime.datetime.utcnow(), color=0xFF9900)
            created_em.set_author(name=f"Ticket", icon_url=reaction.author.avatar_url)
            await reaction.author.send(embed=created_em)
            def check2(m): return m.channel.id==tmsg.channel.id
            reaction2 = await self.client.wait_for("reaction", check=check2)
            if reaction2=="🔒":
                with open('data.json') as f: data = json.load(f)
                if reaction.channel.id in data["ticket-channel-ids"]: channel_id = reaction.channel.id
                await reaction.channel.delete()
                index = data["ticket-channel-ids"].index(channel_id)
                del data["ticket-channel-ids"][index]
                with open('data.json', 'w') as f: json.dump(data, f)

def setup(client):
    client.add_cog(Rticket(client))
