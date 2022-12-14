import inspect
import io
import textwrap
import traceback
from contextlib import redirect_stdout
import aiohttp
import discord
from discord.ext import commands
import datetime

class Eval(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='eval', usage=",eval [kommand]")
    async def _eval(self, ctx, *, body):
        if ctx.author.id == 406137394228625419 or ctx.author.id == 693076081992925234 or ctx.author.id == 609764483229024297 or ctx.author.id == 654721418273226793 or ctx.author.id == 648168353453572117 or ctx.author.id == 710145122460762163:
            """Evaluates python code"""
            env = {
                'ctx': ctx,
                'client': self.client,
                'channel': ctx.channel,
                'author': ctx.author,
                'guild': ctx.guild,
                'message': ctx.message,
                'source': inspect.getsource
            }
            def cleanup_code(content):
                """Automatically removes code blocks from the code."""
                # remove ```py\n```
                if content.startswith('```') and content.endswith('```'):
                    return '\n'.join(content.split('\n')[1:-1])
                # remove `foo`
                return content.strip('` \n')
            env.update(globals())
            body = cleanup_code(body)
            stdout = io.StringIO()
            err = out = None
            to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
            def paginate(text: str):
                '''Simple generator that paginates text.'''
                last = 0
                pages = []
                for curr in range(0, len(text)):
                    if curr % 1980 == 0:
                        pages.append(text[last:curr])
                        last = curr
                        appd_index = curr
                if appd_index != len(text)-1:
                    pages.append(text[last:curr])
                return list(filter(lambda a: a != '', pages))
            try:
                exec(to_compile, env)
            except Exception as e:
                err = await ctx.reply(f'```py\n{e.__class__.__name__}: {e}\n```')
                return await ctx.message.add_reaction('\u2049')
            func = env['func']
            try:
                with redirect_stdout(stdout):
                    ret = await func()
            except Exception as e:
                value = stdout.getvalue()
                err = await ctx.reply(f'```py\n{value}{traceback.format_exc()}\n```')
            else:
                value = stdout.getvalue()
                if ret is None:
                    if value:
                        try:
                            out = await ctx.reply(f'```py\n{value}\n```')
                        except:
                            paginated_text = paginate(value)
                            for page in paginated_text:
                                if page == paginated_text[-1]:
                                    out = await ctx.reply(f'```py\n{page}\n```')
                                    break
                                await ctx.reply(f'```py\n{page}\n```')
                else:
                    try:
                        out = await ctx.reply(f'```py\n{value}{ret}\n```')
                    except:
                        paginated_text = paginate(f"{value}{ret}")
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.reply(f'```py\n{page}\n```')
                                break
                            await ctx.reply(f'```py\n{page}\n```')
            if out:
                await ctx.message.add_reaction('\u2705')  # tick
            elif err:
                await ctx.message.add_reaction('\u2049')  # x
            else:
                await ctx.message.add_reaction('\u2705')
        else:
            embed = discord.Embed(title="Hi??nyz?? jogok", description=f"Nincs elegend?? jogod a parancs v??grehajt??s??hoz!", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
            return

def setup(client):
    client.add_cog(Eval(client))
