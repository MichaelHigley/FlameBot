#Discord Bot for voting on flame
#Bot to keep track of number of flammatory messages of users in server
# ~vote user {quote} to send a text message in chat with their message and vote emojis reacted
# At end of timer, the votes are tallied and either incremented for specified user or not incremented
# If tied, uses sentiment checker to score against them or not
# Bot can also check any users stats with ~tally user to check their tallys
# Can display all users in server with ~tallyall
# Timer lasts for 5 mins
import os
import discord
import datetime
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='~', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='vote', help='~vote user "message here". Then vote using emotes')
async def flamecheck(ctx, *args):
    arguments = ' '.join(args)
    embed = discord.Embed(title="Vote",
                    description='\"' + arguments + '\"',
                    color=ctx.author.color,
                    timestamp=datetime.datetime.now())

            
    msg = await ctx.send('Vote whether this is flame or not: \n' + '\"' + arguments + '\"')
    await msg.add_reaction('✅')
    await msg.add_reaction('❎')
bot.run(TOKEN)

