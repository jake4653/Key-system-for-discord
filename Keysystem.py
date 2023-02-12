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
    embed = discord.Embed(title="Key was created", description=f"Here's the key: {key}", color=0xe74c3c)
    await ctx.send(embed=embed)
@bot.command()
async def redeem(ctx, key: str):
    role = discord.utils.get(ctx.guild.roles, id=1041197916183871498)
    try:
        with open('keys.txt', 'r') as f:
            for line in f:
                try:
                    k, d = line.strip().split()
                except ValueError:
                    # Handle the error
                    continue
                if k == key:
                    await ctx.author.add_roles(role)
                    embed = discord.Embed(title="Role was given", description=f"Role given to daddy {ctx.author}", color=0xe74c3c)
                    await ctx.send(embed=embed)
                    asyncio.create_task(remove_role_after_duration(ctx.author, role, d))
                    break
            else:
                embed = discord.Embed(title="Key doesn't work", description="The key you entered was not valid.", color=0xe74c3c)
                await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="Error Occurred ):", description=f"An error occurred: {e}\n\nPlease contact the owner", color=0xe74c3c)
        await ctx.send(embed=embed)

async def remove_role_after_duration(user, role, duration):
    duration_map = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
    unit = duration[-1]
    if unit not in duration_map:
        return
    duration = int(duration[:-1]) * duration_map[unit]
    await asyncio.sleep(duration)
    await user.remove_roles(role)
    await user.send("__**Your key has expired for Balls server. Rebuy if you want the role back ;)**__")
@bot.command()
async def status(ctx, key: str):
    with open('keys.txt', 'r') as f:
        for line in f:
            try:
                k, d = line.strip().split()
                expiry_time = calculate_expiry_time(d)
            except ValueError:
                # Handle the error
                continue
            if k == key:
                embed = discord.Embed(title="Key status", color=0xe74c3c)
                embed.add_field(name="Key", value=key)
                embed.add_field(name="Expiry time", value=expiry_time)
                await ctx.send(embed=embed)
                break
        else:
            embed = discord.Embed(title="Key doesn't work", description="The key you entered was not valid.", color=0xe74c3c)
            await ctx.send(embed=embed)

def calculate_expiry_time(duration):
    import datetime
    duration_map = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
    unit = duration[-1]
    if unit not in duration_map:
        return
    duration = int(duration[:-1]) * duration_map[unit]
    expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=duration)
    return expiry_time.strftime("%Y-%m-%d\n%H:%M:%S")


bot.run('yourbotoken')

