import time

import nextcord
from nextcord.ext import commands

import settings_controller
from cogs.loops import Loops

from instagrapi import Client


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        cl = Client()
        cl.login('', '')
        print(f'Ready {self.bot.user}')

        while True:
            # try:
            await self.bot.change_presence(
                activity=nextcord.Activity(
                    type=nextcord.ActivityType.playing,
                    name='use /help or /setup to get started')
            )
            l = Loops(self.bot)

            while True:
                print('running instagram')
                await l.instagram_notifier(client=cl)
                print('running twitter')
                await l.twitter_notifier()
                time.sleep(10)
            # except RuntimeError:
            #     pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        settings_controller.add_default(str(guild.id))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        settings_controller.remove_settings(str(guild.id))


def setup(bot):
    bot.add_cog(Events(bot))
