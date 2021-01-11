import discord
import json
import os
import random
from discord.ext import commands
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
import youtube_dl

from random import choice

TOKEN = 'NjkyMzMzMDM2NzUwMTEwNzgy.Xns_Yg.M5WCcE0ikHaXnRmiaGjPMQGS3bw'

client = commands.Bot(command_prefix = 'r!')
client.remove_command("help")

me = 339315178271277058

@client.event
async def on_ready():
    
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over the mods and my prefix is r! 👀")) 
    print(f'{client.user} the bot is ready!')

@client.command()
async def help(ctx):
  embed=discord.Embed(title="Help", description="This command shows you all the commands you need to know", color=0x32CDD7)
  embed.add_field(name="r!update", value="``This will show you what version the bot is``", inline=False)
  embed.add_field(name="r!help_fun", value="``This will show you the fun commands``", inline=False)
  embed.add_field(name="r!help_mod", value="``This will show you the moderator commands``", inline=False)
  await ctx.send(embed=embed)

@client.command()
async def help_fun(ctx):
  embed=discord.Embed(title="Fun Commands", description="This command shows you the fun commands", color=0x00FF00)
  embed.add_field(name="r!whois", value="``This message will show your account when you made it and what time and shows you yuor roles``", inline=False)
  await ctx.send(embed=embed)

@client.command()
async def help_mod(ctx):
  embed=discord.Embed(title="Moderator Commands", description="This command shows you the moderator commands", color=0x7FFFD4)
  embed.add_field(name="r!clear", value="``This message clear``", inline=False)
  embed.add_field(name="r!kick", value="``This command lets you kick people``", inline=False)
  embed.add_field(name="r!ban", value="``This command lets you ban people``", inline=False)
  await ctx.send(embed=embed)

@client.command(name='join', help='This command makes the bot join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return

    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

@client.command(name='leave', help='This command stops makes the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

@client.command()
async def update(ctx):
  embed=discord.Embed(title="Update", description="Bot version 0.1", color=0xff0000)
  await ctx.send(embed=embed)

@client.command(aliases=['c'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit = amount)

@client.command(aliases=['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason= "No reason provided"):
    await member.send("You have been kicked from the group, Because:"+reason)
    await member.kick(reason=reason)

@client.command(aliases=['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason= "No reason provided"):
    await ctx.send(member.name +" have been Banned from the group, Because:"+reason)
    await member.ban(reason=reason)

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        embed = discord.Embed(title="Error", description=":x: You don't have permission to kick members.",color=discord.Color.red())
        await ctx.send(embed=embed)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        embed = discord.Embed(title="Error", description=":x: You don't have permission to clear chat.",color=discord.Color.red())
        await ctx.send(embed=embed)

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        embed = discord.Embed(title="Error", description=":x: You don't have permission to Ban members.",color=discord.Color.red())
        await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    await ctx.send(f'Your ping is {round(client.latency * 1000)}ms')
    
@client.command(name="userinfo", aliases=['ui', 'whois', 'who', 'info'])
@commands.has_permissions(administrator = True)
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    embed = discord.Embed(
        color=discord.Colour.red(),
        timestamp=ctx.message.created_at,
        description=member.mention
    )

    embed.set_author(name=f"{member} Info")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(
        text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=member.id, inline=False)
    embed.add_field(
        name="Registered At:",
        value=member.created_at.strftime("%a, %d %b %Y %I:%M %p"),
        inline=False
    )
    embed.add_field(
        name="Joined Server At:",
        value=member.joined_at.strftime("%a, %d %b %Y %I:%M %p"),
        inline=False
    )

    roles = " ".join([role.mention for role in member.roles if role != ctx.guild.default_role])

    if len(roles.strip()) == 0:
        roles = "This user does not have any roles"

    embed.add_field(
        name=f"{len(member.roles)-1} Roles",
        value=roles,
        inline=False
    )
    embed.add_field(name="Bot?", value=member.bot)

    await ctx.send(embed=embed)

@client.command()
async def say(ctx, *, msg):
    await ctx.message.delete()
    await ctx.send("{}" .format(msg))

client.run(TOKEN)

