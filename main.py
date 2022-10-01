import os

import nextcord
from nextcord.ext import commands

BEARER_TOKEN = os.environ['BEARER_TOKEN']  # hidden environment variables
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(intents=intents)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')  # loading cogs
bot.run(DISCORD_TOKEN)
