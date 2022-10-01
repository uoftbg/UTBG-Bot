import nextcord
from nextcord.ext import commands

import settings_controller
from cogs.loops import Loops


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Ready {self.bot.user}')
        try:
            await self.bot.change_presence(
                activity=nextcord.Activity(
                    type=nextcord.ActivityType.playing,
                    name='use /help or /setup to get started')
            )
            await Loops.twitter_notifier.start(self)
        except RuntimeError:
            pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        settings_controller.add_default(str(guild.id))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        settings_controller.remove_settings(str(guild.id))


def setup(bot):
    bot.add_cog(Events(bot))
