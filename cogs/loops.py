from instagrapi import Client
from nextcord.ext import commands

import discord_manager
import embed_manager
import file_manager
import thumbnails
import tweet_manager


class Loops(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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
                                                   webhooks_dict,
                                                   )

    async def instagram_notifier(self, client: Client):

        old_post_ids = file_manager.load('json/instagram.json')

        follower_count = client.user_info_by_username('uoftbg').dict()[
            'follower_count']

        posts = client.user_medias(user_id=51719050363,
                                   amount=10)  # pulling last 10 posts of uoftbg

        updated_post_ids = [post.pk for post in posts]

        new_post_ids = set(updated_post_ids) - set(old_post_ids)

        if len(new_post_ids) != 0:  # number of new posts is not 0
            file_manager.save('json/instagram.json',
                              updated_post_ids)  # update to dict later

        for new_post_id in list(new_post_ids):
            print(new_post_id)

            media_urls = []

            media_info = client.media_info(int(new_post_id))

            username = media_info.user.username
            profile_pic_url = media_info.user.profile_pic_url
            author_url = f'https://www.instagram.com/{username}/'

            caption = media_info.caption_text
            if not media_info.resources:  # only one picture
                media_urls = [str(media_info.thumbnail_url)]

            else:  # more than one picture
                for resource in media_info.resources:  # getting all media urls
                    media_urls.append(str(resource.thumbnail_url))
            print('media urls: ', media_urls)

            embed = embed_manager.create_instagram_embed(
                caption=caption,
                media_urls=media_urls,
                author_name=username,
                author_url=author_url,
                author_icon_url=profile_pic_url
            )

            webhooks_dict = file_manager.load('json/webhooks.json')

            guild_id = 574362160415768576

            await discord_manager.send_webhook(
                embed=embed,
                avatar_url=thumbnails.BOT_ICON,
                guild_id=guild_id,
                screen_name=username,
                to_ping='',
                webhooks_dict=webhooks_dict
            )
        return


def setup(bot):
    bot.add_cog(Loops(bot))
