import discord
import asyncio
import random
import tinydb
import datetime
from discord.ext import commands

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

db = tinydb.TinyDB('keys.json')

@bot.command()
async def createkey(ctx, duration: str):
    key = ''.join(random.choices(['a', 'b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5', '6'], k=24))
    db.insert({'key': key, 'duration': duration, 'used': False, 'expiration_timestamp': 0})
    embed = discord.Embed(title="Key was created", description=f"Here's the key: {key}", color=0xe74c3c)
    await ctx.send(embed=embed)

@bot.command()
async def redeem(ctx, key: str):
    role = discord.utils.get(ctx.guild.roles, id=1041197916183871498)
    record = db.search(tinydb.Query().key == key)
    if record:
        record = record[0]
        if not record['used']:
            await ctx.author.add_roles(role)
            embed = discord.Embed(title="Role was given", description=f"Role given to {ctx.author}", color=0xe74c3c)
            await ctx.send(embed=embed)
            duration = calculate_duration(record['duration'])
            db.update({'used': True, 'expiration_timestamp': int(datetime.datetime.now().timestamp()) + duration}, tinydb.Query().key == key)
            asyncio.create_task(remove_role_after_duration(ctx.author, role, duration))
        else:
            embed = discord.Embed(title="Sorry this key has been used", description="The key you entered was already used\nStop trying to snipe :sob:", color=0xe74c3c)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Key doesn't work", description="The key you entered was not valid.", color=0xe74c3c)
        await ctx.send(embed=embed)

async def remove_role_after_duration(user, role, duration):
    await asyncio.sleep(duration)
    if role in user.roles:
        await user.remove_roles(role)
        await user.send("__**Your key has expired for Balls server. Rebuy if you want the role back ;)**__")

def calculate_duration(duration):
    duration_map = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
    unit = duration[-1]
    if unit not in duration_map:
        return
    duration = int(duration[:-1]) * duration_map[unit]
    return duration

@bot.command()
async def status(ctx, key: str):
    record = db.search(tinydb.Query().key == key)
    if record:
        record = record[0]
        if not record['used']:
            embed = discord.Embed(title="Key status", description=f"Key not used", color=0xe74c3c)
            await ctx.send(embed=embed)
        else:
            expiration_timestamp = record['expiration_timestamp']
            expiration_datetime = datetime.datetime.fromtimestamp(expiration_timestamp)
            embed = discord.Embed(title="Key status", description=f"Expiration date: {expiration_datetime.strftime('%Y-%m-%d %H:%M:%S')}", color=0xe74c3c)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Key status", description=f"Key not found", color=0xe74c3c)
        await ctx.send(embed=embed)


bot.run('token')
