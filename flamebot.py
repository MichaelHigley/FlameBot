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
import numpy as np
import json
import requests
import random
from dotenv import load_dotenv
from discord.ext import commands, tasks
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API_LINK_PA = 'https://api.open-meteo.com/v1/forecast?latitude=37.44&longitude=-122.14&daily=temperature_2m_max,temperature_2m_min&current_weather=true&temperature_unit=fahrenheit&&timezone=America%2FLos_Angeles'

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='~', intents=intents, help_command=None)

#tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
#model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")

utc = datetime.timezone.utc
time = datetime.time(hour=15, minute=0, tzinfo=utc)

df = np.loadtxt('cutemessages.txt',dtype=str, delimiter='\n')
USERID = np.loadtxt('userid.txt', dtype=str)

class scheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.my_task.start()

    def cog_unload(self):
        self.my_task.cancel()

    @tasks.loop(hours=24)
    async def my_task(self):
        print("task is running!")
        response = requests.get(API_LINK_PA)
        test = (response.json())
        current_temp = test['current_weather']['temperature']
        max_temp = test['daily']['temperature_2m_max'][0]
        min_temp = test['daily']['temperature_2m_min'][0]
        user = await bot.fetch_user("USERID")
        await user.send('Here\'s your daily weather and morning note:')
        await user.send('The temperature right now in Palo Alto is ' + str(current_temp) + '°F while the low is ' + str(min_temp) + '°F and there\'s a high of ' + str(max_temp) + '°F')
        await user.send(df[random.randrange(21)])
        
        
testing = scheduler(bot)
#testing.my_task.start()

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
    #embed.add_field()
    msg = await ctx.send('Vote whether this is flame or not: \n' + '\"' + arguments + '\"')

    """
    inputs = tokenizer(arguments, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    model.config.id2label[predicted_class_id]
    """
    await msg.add_reaction('✅')
    await msg.add_reaction('❎')


bot.run(TOKEN)


