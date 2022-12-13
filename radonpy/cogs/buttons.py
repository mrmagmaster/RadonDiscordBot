from os import replace
import discord
from discord.ext import commands
from discord_components import *
import datetime
import json

class Buttons(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def btnticketsetup(self, ctx, csatorna: discord.TextChannel):
        components1 = [ Button(label=":ticket:"), Button(label=":lock:") ]
        embed=discord.Embed(title="Ticket", description="Reagálj a :ticket: emojival a ticket létrehozásához!", color=0xff9900)
        embed.set_footer(icon_url=self.client.user.avatar_url, text="Radon × Ticket")
        global msg
        msg = await csatorna.send(embed=embed, components=components1[0])
        interaction = await self.client.wait_for("button_click")
        if interaction:
            with open("data.json") as f: data = json.load(f)
            ticket_number = int(data["ticket-counter"])
            ticket_number += 1
            ticket_channel = await interaction.guild.create_text_channel(f"ticket-{interaction.author}")
            await ticket_channel.set_permissions(interaction.guild.get_role(interaction.guild.id), send_messages=False, read_messages=False)
            for role_id in data["valid-roles"]:
                role = interaction.guild.get_role(role_id)
                await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True, manage_channel=True)
            await ticket_channel.set_permissions(interaction.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
            tmsg=await ticket_channel.send(f"{interaction.author.mention}, a ticketed elkészült! Lezárás a :lock: emojival.", components=components1[1])
            pinged_msg_content = ""
            non_mentionable_roles = []
            if data["pinged-roles"] != []:
                for role_id in data["pinged-roles"]:
                    role = interaction.guild.get_role(role_id)
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
            created_em.set_author(name=f"Ticket", icon_url=interaction.author.avatar_url)
            await interaction.author.send(embed=created_em)
            reaction2 = await self.client.wait_for("button_click")
            if reaction2=="🔒":
                with open('data.json') as f: data = json.load(f)
                if interaction.channel.id in data["ticket-channel-ids"]: channel_id = interaction.channel.id
                await interaction.channel.delete()
                index = data["ticket-channel-ids"].index(channel_id)
                del data["ticket-channel-ids"][index]
                with open('data.json', 'w') as f: json.dump(data, f)

    @commands.command(aliases=["számológép","btncalc","gombszámológép","buttoncalculator","buttoncalc","gombszámoló"])
    async def szamologep(self, ctx):
        if not ctx.author.id == 406137394228625419: return
        numbers = []
        muvelet = []
        components = [
            [ Button(label="7"), Button(label="8"), Button(label="9"), Button(label="÷", style=ButtonStyle.blue)  ],
            [ Button(label="4"), Button(label="5"), Button(label="6"), Button(label="*", style=ButtonStyle.blue)  ], 
            [ Button(label="1"), Button(label="2"), Button(label="3"), Button(label="-", style=ButtonStyle.blue) ],
            [ Button(label="X", style=ButtonStyle.red), Button(label="0"), Button(label="=", style=ButtonStyle.green), Button(label="+", style=ButtonStyle.blue) ],
            [ Button(label=",", style=ButtonStyle.blue), Button(label="C", style=ButtonStyle.blue), Button(label="AC", style=ButtonStyle.blue), Button(label="INFÓ", style=ButtonStyle.blue) ]
        ]
        embed = discord.Embed(description="``` 0 ```", color=0xff9900)
        embed.set_author(name="Számológép", icon_url=ctx.author.avatar_url)
        
        msg = await ctx.reply(embed=embed, components=components, mention_author=False)
        
        while True:
            interaction = await self.client.wait_for("button_click", check = lambda i: i.author.id == ctx.author.id)
            nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            if interaction.component.label in nums: numbers.append(interaction.component.label)
            else: 
                if interaction.component.label == "÷":
                    muvelet.append("/")
                else: muvelet.append(interaction.component.label)
            if len(muvelet) == 0: embed = discord.Embed(title="Számológép", description=f"``` {numbers[0]} ```")
            else: 
                try: embed = discord.Embed(title="Számológép", description=f"``` {numbers[0]} {muvelet[0]} {numbers[1]} ```")
                except: embed = discord.Embed(title="Számológép", description=f"``` {numbers[0]} {muvelet[0]} ```")
            if interaction.component.label == "=":
                if muvelet[0] == "/":
                    eredmeny = int(numbers[0]) / int(numbers[1])
                    embed = discord.Embed(title="Számológép", description=f"``` {eredmeny} ```")
                    await interaction.respond(type=InteractionType.UpdateMessage, content=None, embed=embed, components=components)
                    numbers.clear()
                    muvelet.clear()
                if muvelet[0] == "+":
                    eredmeny = int(numbers[0]) + int(numbers[1])
                    embed = discord.Embed(title="Számológép", description=f"``` {eredmeny} ```")
                    await interaction.respond(type=InteractionType.UpdateMessage, content=None, embed=embed, components=components)
                    numbers.clear()
                    muvelet.clear()
                if muvelet[0] == "-":
                    eredmeny = int(numbers[0]) - int(numbers[1])
                    embed = discord.Embed(title="Számológép", description=f"``` {eredmeny} ```")
                    await interaction.respond(type=InteractionType.UpdateMessage, content=None, embed=embed, components=components)
                    numbers.clear()
                    muvelet.clear()
                if muvelet[0] == "*":
                    eredmeny = int(numbers[0]) * int(numbers[1])
                    embed = discord.Embed(title="Számológép", description=f"``` {eredmeny} ```")
                    await interaction.respond(type=InteractionType.UpdateMessage, content=None, embed=embed, components=components)
                    numbers.clear()
                    muvelet.clear()
                
            else:
                await interaction.respond(type=InteractionType.UpdateMessage, content=None, embed=embed, components=components)

def setup(client):
    client.add_cog(Buttons(client))
