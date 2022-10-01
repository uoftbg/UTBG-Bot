from nextcord.ext import commands, tasks

import discord_manager
import embed_manager
import file_manager
import tweet_manager


class Loops(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=10)
    async def twitter_notifier(self):
        twitter_users_dict = file_manager.load('json/twitterUsers.json')
        options_dict = file_manager.load('json/options.json')
        webhooks_dict = file_manager.load('json/webhooks.json')

        for screen_name in twitter_users_dict.keys():
            user_id, last_tweet_id = tweet_manager.retrieve_last_tweet_id_user_id(
                screen_name)

            is_new_tweet = tweet_manager.is_new_tweet(user_id, last_tweet_id)
            if not is_new_tweet:
                continue

            tweet_manager.store_in_database(user_id, last_tweet_id)

            embed_info = tweet_manager.convert_to_embed_info(
                screen_name, last_tweet_id)

            embed = embed_manager.create_embed(tweet_title=embed_info[0],
                                               author_name=embed_info[1],
                                               author_url=embed_info[2],
                                               author_icon_url=embed_info[3],
                                               attachment_url=embed_info[4]
                                               )

            for guild_id in twitter_users_dict[screen_name]:

                if tweet_manager.is_quote_tweet(screen_name) and (
                        options_dict[str(guild_id)][screen_name][
                            'include_quote_tweets'] == 'False'):
                    continue

                to_ping = discord_manager.get_ping(guild_id, screen_name)

                await discord_manager.send_webhook(embed, embed_info[3],
                                                   guild_id,
                                                   screen_name, to_ping,
                                                   webhooks_dict)


def setup(bot):
    bot.add_cog(Loops(bot))
