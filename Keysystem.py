import discord
import asyncio
import random
from discord.ext import commands

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

@bot.command()
async def createkey(ctx, duration: str):
    key = ''.join(random.choices(['a', 'b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5', '6'], k=24))
    with open('keys.txt', 'a') as f:
        f.write(f'{key} {duration}\n')
    await ctx.send(f'Key created: {key}')

@bot.command()
async def redeem(ctx, key: str):
    role = discord.utils.get(ctx.guild.roles, id=yourroleidhere)
    with open('keys.txt', 'r') as f:
        for line in f:
            k, d = line.strip().split()
            if k == key:
                await ctx.author.add_roles(role)
                await ctx.send(f'Role added to {ctx.author}')
                asyncio.create_task(remove_role_after_duration(ctx.author, role, d))
                break
        else:
            await ctx.send('Key not found')

async def remove_role_after_duration(user, role, duration):
    duration_map = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
    unit = duration[-1]
    if unit not in duration_map:
        return
    duration = int(duration[:-1]) * duration_map[unit]
    await asyncio.sleep(duration)
    await user.remove_roles(role)

bot.run('token')
