import discord
import asyncio
import random
import tinydb
import datetime
from discord.ext import commands
from random import randint
bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())
gay = random.randint(45,95)
token = "TOKEN-HERE"
db = tinydb.TinyDB('keys.json')

@bot.command()
async def createkey(ctx, duration: str):
    key = ''.join(random.choices(['a', 'b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5', '6'], k=24))
    db.insert({'key': key, 'duration': duration, 'used': False, 'expiration_timestamp': 0})
    
    embed = discord.Embed(title="Key Created", description=f"Here's your key master: `{key}`\n\n*Made by Semai*", color=0x9b59b6)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1074008649346850886/1075521628852715620/giphy.gif")
    embed.set_footer(text="Expires in: " + duration)
    await ctx.send(embed=embed)

@bot.command()
async def redeem(ctx, key: str):
    role = discord.utils.get(ctx.guild.roles, id=YOURROLEIDHERE)
    record = db.search(tinydb.Query().key == key)
    if record:
        record = record[0]
        if not record['used']:
            await ctx.author.add_roles(role)
            duration = calculate_duration(record['duration'])
            db.update({'used': True, 'expiration_timestamp': int(datetime.datetime.now().timestamp()) + duration}, tinydb.Query().key == key)
            asyncio.create_task(remove_role_after_duration(ctx.author, role, duration))

            embed = discord.Embed(title="Role Given", description=f"Role granted to master {ctx.author.mention}\nBtw you are {gay}% gay don't ask why", color=0x9b59b6)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1074008649346850886/1075521628852715620/giphy.gif")
            embed.set_footer(text=f"Expires in: {record['duration']}  Made by Semai")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Invalid Key", description="The key you entered was already used.\nStop trying to snipe! 😭\n\nMade by Semai", color=0xe74c3c)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Invalid Key", description="The key you entered was not valid.\n\nMade by Semai", color=0xe74c3c)
        await ctx.send(embed=embed)

async def remove_role_after_duration(user, role, duration):
    await asyncio.sleep(duration)
    if role in user.roles:
        await user.remove_roles(role)
        await user.send("Your key has expired for popo predictor!    *This is just a reminder*")

def calculate_duration(duration):
    duration_map = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'y': 31536000, }
    unit = duration[-1]
    if unit not in duration_map:
        return
    duration = int(duration[:-1]) * duration_map[unit]
    return duration

@bot.command()
async def cmds(ctx):
    embed=discord.Embed(color=0x9b59b6)
    pfp = 'https://cdn.discordapp.com/attachments/1074008649346850886/1075521628852715620/giphy.gif'
    embed.set_thumbnail(url=pfp)
    embed.add_field(name="*Commands*", value=f"""\n\n.createkey (duration)\nMakes key\n\n.reedem (key)\nRedeems the key)""")
    embed.set_footer(text="Made by Semai")
    await ctx.reply(embed=embed)

bot.run(token)
