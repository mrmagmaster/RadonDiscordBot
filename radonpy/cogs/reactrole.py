import discord
from discord.ext import commands
import json
import datetime
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

class ReactRole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            pass
        else:
            with open('reactrole.json') as react_file:
                data = json.load(react_file)
                for x in data:
                    if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
                        role = discord.utils.get(self.client.get_guild(payload.guild_id).roles, id=x['role_id'])
                        await payload.member.add_roles(role)
                        szerver = self.client.get_guild(payload.guild_id)
                        await payload.member.send(f'Sikeresen rádadtam a `{role}` rangot a **{szerver}** szerveren!')

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        with open('reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
                    role = discord.utils.get(self.client.get_guild(payload.guild_id).roles, id=x['role_id'])
                    szerver = self.client.get_guild(payload.guild_id)
                    member = await szerver.fetch_member(payload.user_id)
                    await member.remove_roles(role)
                    await member.send(f'Sikeresen elvettem a `{role}` rangot a **{szerver}** szerveren!')

    @commands.command(usage=",reactrole [emoji (nem nitrós!)] [rang] [üzenet]", aliases=["react","normalreactrole","reactionrole","simareakciórang","reakció"])
    async def reactrole(self, ctx, emoji, role: discord.Role, *, message):
        if ctx.author.guild_permissions.manage_roles:
            emb = discord.Embed(description=message)
            msg = await ctx.channel.send(embed=emb)
            await msg.add_reaction(emoji)
            with open('reactrole.json') as json_file:
                data = json.load(json_file)
                new_react_role = {'role_name': role.name, 
                'role_id': role.id,
                'emoji': emoji,
                'message_id': msg.id}
                data.append(new_react_role)
            with open('reactrole.json', 'w') as f:
                json.dump(data, f, indent=4)
        else:
            perm = "Rangok kezelése"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
            return

def setup(client):
    client.add_cog(ReactRole(client))
