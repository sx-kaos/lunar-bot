import time
import random
import os
import asyncio
import colorama
import sys
import discord
from discord.ext import commands
from os import system
from datetime import datetime
from datetime import date
from datetime import datetime
from typing import Optional
from discord import Embed, Member
from discord.ext.commands import Cog
from colorama import init
from pypresence import Presence
from discord.utils import find
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions

client = commands.Bot(command_prefix = '>')

colorama.init()

RPC = Presence("856168902803587082") 
RPC.connect() 
RPC.update(
large_image="untitled",


buttons = [
        {"label": "Discord", "url": "https://dsc.gg/kaos"}
],
start=time.time()
)

print(f"""\033[1;32;40m
						▄▄▌  ▄• ▄▌ ▐ ▄  ▄▄▄· ▄▄▄  
						██•  █▪██▌•█▌▐█▐█ ▀█ ▀▄ █·
						██▪  █▌▐█▌▐█▐▐▌▄█▀▀█ ▐▀▀▄ 
						▐█▌▐▌▐█▄█▌██▐█▌▐█ ▪▐▌▐█•█▌
						.▀▀▀  ▀▀▀ ▀▀ █▪ ▀  ▀ .▀  ▀
""")


@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member} Was kicked for "{reason}"')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You Do Not Have The Right Permissions To Use This Command")

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member} Was Banned for "{reason}"')

@kick.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You Do Not Have The Right Permissions To Use This Command")

@client.command()
async def ping(ctx):
  await ctx.send(f'{round(client.latency * 1000)}ms')


@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="muted")

   await member.remove_roles(mutedRole)
   await member.send(f" you have unmutedd from: - {ctx.guild.name}")
   embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",colour=discord.Colour.light_gray())
   await ctx.send(embed=embed)

@client.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=True, send_messages=False, read_message_history=True, read_messages=True)
    embed = discord.Embed(title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" you have been muted from: {guild.name} reason: {reason}")


@client.command()
async def clear(ctx, amount : int):
        await ctx.channel.purge(limit=amount)


@client.command()
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user


    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f'unbanned {user.mention}')
      return

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('>help'))

client.remove_command('help')

@client.command()
async def help(ctx):
	embed=discord.Embed(title="𝗵𝗲𝗹𝗽", color=0x5fd3e0)
	embed.add_field(name=">help_mod", value="shows moderator commands", inline=False)
	embed.add_field(name=">help_normal", value="shows commands for anyone to use", inline=True)
	embed.set_footer(text="bot made by kaos")
	await ctx.send(embed=embed)

@client.command()
async def help_normal(ctx):
	embed=discord.Embed(title="𝗵𝗲𝗹𝗽 𝗻𝗼𝗿𝗺𝗮𝗹", description=" ", color=0x5fd3e0)
	embed.set_author(name=" ")
	embed.add_field(name=">ping", value="displays ping", inline=False)
	embed.add_field(name=">password", value="shows how long it would take to hack a password based on length, e.g. >password 4 ", inline=True)
	embed.add_field(name=">meme", value="sends a random meme", inline=False)
	embed.add_field(name=">rng", value="sends a random number 1-100", inline=False)
	embed.add_field(name=">serverinfo", value="sends server info", inline=True)
	embed.add_field(name=">user", value="shows info about the user mentioned, e.g. >info @someone", inline=False)
	embed.set_footer(text="bot made by kaos")
	await ctx.send(embed=embed)

@client.command()
async def help_mod(ctx):
	embed=discord.Embed(title="𝗵𝗲𝗹𝗽 𝗺𝗼𝗱", description=" ", color=0x5fd3e0)
	embed.set_author(name=" ")
	embed.add_field(name=">ban", value="bans the user mentioned", inline=False)
	embed.add_field(name=">unban", value=" unbans the user mentioned", inline=True)
	embed.add_field(name=">kick", value="kicks the user mentioned", inline=False)
	embed.add_field(name=">lockdown", value="locks the channel the command is used in", inline=False)
	embed.add_field(name=">unlock", value="unlocks the channel the command is used in", inline=True)
	embed.add_field(name=">clear", value="deletes a certain amount of messages, e.g. >clear 50", inline=False)
	embed.add_field(name=">mute", value="mutes the user mentioned", inline=True)
	embed.add_field(name=">unmute", value="unmutes the user mentioned", inline=False)
	embed.set_footer(text="bot made by kaos")
	await ctx.send(embed=embed)

@client.command(pass_context = True)
async def rng(ctx):
    embed = discord.Embed(title = "Random Number", description = (random.randint(1, 100)), color = (0xF85252))
    await ctx.send(embed = embed)

@client.command(aliases=['meme'])
async def _meme(ctx):
    responses = [ 'https://preview.redd.it/oy4nqdoudoz61.jpg?width=640&crop=smart&auto=webp&s=3df0e04fa81bfba97f457af7d9b46e60cca80380',
                  'https://preview.redd.it/iufury6njnz61.jpg?width=640&crop=smart&auto=webp&s=d393ed6ccb951722743dff2181aaf5e7e09d074f',
                  'https://preview.redd.it/zju1xt921mz61.jpg?width=640&crop=smart&auto=webp&s=07ebbafad02b21e9ff8bb94e88fbd2b4180d8da8',
                  'https://pbs.twimg.com/profile_images/3417714567/46298b9ed1c056537d7a0ab67176ffd7_400x400.jpeg',
                  'https://cdn.discordapp.com/attachments/839508203665621014/843910798988410921/2Q.png',
                  'https://cdn.discordapp.com/attachments/839508203665621014/843910886225084417/funnyrapememe.png',
                  'https://64.media.tumblr.com/e66ac627fbd5824bc9fd579b06fc9cde/tumblr_owziyjVRna1ub0po4o1_400.jpg',
                  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRcG5T7X4oteJyFK8RkHwe7Zh74TejRzm_57w&usqp=CAU',
                  'https://www.dailymoss.com/wp-content/uploads/2017/12/1F42DE2C-D7F4-467C-A3CC-F916DD1229E1.jpg',
                  'https://pics.me.me/me-posts-an-offensive-meme-me-people-who-enjoy-dark-46889882.png',
                  'https://cdn.discordapp.com/attachments/800789841859575810/846084875924668488/3a728efcfc2ab94ef46cc6d4e6adc05a.png',
                  'https://i.pinimg.com/originals/17/25/62/1725628658704672a5c5ce86bacf854a.jpg',
                  'https://pbs.twimg.com/media/DXUQOCYW4AA0p9n.jpg',
                  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLVzY9DcY6IcarwoyTtWao2HDrQc1s3mEKMg&usqp=CAU',
                  'https://i.pinimg.com/736x/ec/43/8c/ec438c21d17d10931793755c26313ce5.jpg',
                  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ__MHDSSeaQY_G9MHn3-TEPmuSkPy1uyVBBQ&usqp=CAU',
                  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRVGfIMJD9Ge-EfgYPgcTE14MjEHLzhTXWuvw&usqp=CAU',
                  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ87uGRWr2tyQlM83H4MdwTWWx2FHw_pt4UFA&usqp=CAU',
                  'https://cdn.discordapp.com/attachments/829034757341970544/843912733253959741/zn87xed0f4251.png',
                  'https://pbs.twimg.com/media/DTmET1gVMAAx93x.jpg']
    await ctx.send(f'{random.choice(responses)}')

@client.command()
async def serverinfo(ctx):
  name = str(ctx.guild.name)
  description = ""


  owner = str(ctx.guild.owner)
  id = str(ctx.guild.id)
  region = str(ctx.guild.region)
  memberCount = str(ctx.guild.member_count)

  icon = str(ctx.guild.icon_url)

  embed = discord.Embed(
      title=name + " Server Information",
      description=description,
      color=discord.Color.blue()
    )
  embed.add_field(name="Server ID", value=id, inline=False)
  embed.add_field(name="Region", value=region, inline=True)
  embed.add_field(name="Member Count", value=memberCount, inline=True)

  await ctx.reply(embed=embed)

@client.command()
async def user(ctx, target: Optional[Member]):
    target = target or ctx.author
    embed = Embed(title="User information",
    colour=target.colour,
    timestamp=datetime.utcnow())
    embed.set_thumbnail(url=target.avatar_url)
    fields = [("Name", str(target), True),
    ("ID", target.id, True),
    ("Bot?", target.bot, True),
    ("Top role", target.top_role.mention, True),
    ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
    ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
    ("Boosted", bool(target.premium_since), True)]
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_channels = True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send( ctx.channel.mention + " ***is now in lockdown.***")

@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + " ***has been unlocked.***")

@client.command()
async def password(ctx, *, question):
	now = datetime.now()
	length = int(question)
	length2 = 92 ** int(length)
	if length2 > 15000:
	    await ctx.reply(f'{length2} possible passwords, this may take some time')
	elif length2 < 15000:
	    pass
	x = 1
	while True:
		x += 1
		if x == length2:
			end = datetime.now()
			embed=discord.Embed(title="Password", color=0x47c9cf)
			embed.add_field(name=f"length: ", value=f"{length}", inline=True)
			embed.add_field(name=f"permutations: ", value=f"{length2}", inline=False)
			embed.add_field(name=f"time:", value=f"if the hackers started at {now} they would finish at {end}", inline=True)
			await ctx.reply(embed=embed)
			break
client.run('OTAyODU4ODUwNzkxNzM1MzI3.YXki1A.ldFgqBN4eQYLCE8T5ec4IxMsr5U')
