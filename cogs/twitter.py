import nextcord
from nextcord import ButtonStyle, Interaction, SlashOption
from nextcord.ext import commands
from nextcord.ui import Button, View

import discord_manager
import embed_manager
import file_manager
import thumbnails
import tweet_manager


class Twitter(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='follow',
                            description='Receive twitter feed in a channel')
    async def follow(
            self,
            interaction: Interaction,
            username: str = SlashOption(
                required=True, description='The username of the twitter user'),
            ping: str = SlashOption(
                required=True,
                description='Who should be pinged when this user tweets',
                choices={
                    'Noone': '0',
                    'Only me': '1',
                    'Everyone': '2'
                }),
            include_quote_tweets: str = SlashOption(
                required=True,
                description='Allow quote tweets to be posted',
                choices={
                    'True': 'True',
                    'False': 'False'
                }),
    ):
        if not discord_manager.has_permission(interaction):
            await interaction.response.send_message("You are not authorized to "
                                                    "run this command.",
                                                    ephemeral=True)
            return

        twitter_users_dict = file_manager.load('json/twitterUsers.json')
        options_dict = file_manager.load('json/options.json')

        # invalid twitter username
        if not tweet_manager.check_valid_screen_name(username):
            embed = embed_manager.create_embed_header_footer(
                content='Please enter a correct twitter username.',
                title='Invalid Username.',
                icon_url=thumbnails.RED_X_PNG)
            await discord_manager.send(embed=embed, interaction=interaction)

        # case insensitive

        elif username.casefold() in map(str.casefold,
                                        twitter_users_dict.keys()) and str(
            interaction.guild_id) in \
                twitter_users_dict[username]:
            embed = embed_manager.create_embed_header_footer(
                content='To change tweet options, use /unfollow and /follow.',
                title='Already following this user!',
                icon_url=thumbnails.RED_X_PNG)
            await discord_manager.send(embed=embed, interaction=interaction)

        else:
            try:
                twitter_users_dict[username]
            except KeyError:
                twitter_users_dict[username] = [str(interaction.guild_id)]
            else:
                twitter_users_dict[username].append(str(interaction.guild_id))
            # setting the options

            try:
                options_dict[str(interaction.guild_id)]
            except KeyError:
                options_dict[str(interaction.guild_id)] = {
                    username: {
                        'ping': ping,
                        'ping_user': interaction.user.mention,
                        'include_quote_tweets': include_quote_tweets
                    }
                }
            else:
                options_dict[str(interaction.guild_id)][username] = {
                    'ping': ping,
                    'ping_user': interaction.user.mention,
                    'include_quote_tweets': include_quote_tweets}

            embed = embed_manager.create_embed_header_footer(
                content='You will begin to receive tweets from this user in '
                        'this server.',
                title='Added twitter user to following.',
                icon_url=thumbnails.CHECKMARK_PNG)
            await discord_manager.send(embed=embed, interaction=interaction)

            file_manager.save(f='json/twitterUsers.json',
                              edited_dict=twitter_users_dict)
            file_manager.save(f='json/options.json', edited_dict=options_dict)

    @nextcord.slash_command(name='unfollow',
                            description='Stop receiving twitter feed in a channel')
    async def unfollow(
            self,
            interaction: Interaction,
            username: str = SlashOption(
                required=True,
                description='The username of the twitter user'
            )
    ):
        if not discord_manager.has_permission(interaction):
            await interaction.response.send_message("You are not authorized to "
                                                    "run this command.",
                                                    ephemeral=True)
            return
        twitter_users_dict = file_manager.load('json/twitterUsers.json')
        options_dict = file_manager.load('json/options.json')

        if not tweet_manager.check_valid_screen_name(username):
            embed = embed_manager.create_embed_header_footer(
                content='Please enter a correct twitter username.',
                title='Invalid Username.',
                icon_url=thumbnails.RED_X_PNG)
            await discord_manager.send(embed=embed, interaction=interaction)

        # case insensitive
        elif str(interaction.guild_id) not in options_dict.keys():
            embed = embed_manager.create_embed_header_footer(
                content='Please enter a correct twitter username.',
                title='Not Following this User!',
                icon_url=thumbnails.RED_X_PNG)
            await discord_manager.send(embed=embed, interaction=interaction)

        elif username.casefold() not in map(str.casefold, options_dict[
            str(interaction.guild_id)].keys()):
            embed = embed_manager.create_embed_header_footer(
                content='Please enter a correct twitter username.',
                title='Not Following this User!',
                icon_url=thumbnails.RED_X_PNG)
            await discord_manager.send(embed=embed, interaction=interaction)

        else:

            if len(twitter_users_dict[
                       username]) == 1 and len(twitter_users_dict) == 1:
                twitter_users_dict = {}
            elif len(twitter_users_dict[username]) == 1:
                del twitter_users_dict[username]
            else:
                twitter_users_dict[username].pop(
                    twitter_users_dict[username].index(
                        str(interaction.guild_id)))

            if len(options_dict[str(interaction.guild_id)]) == 1 and len(
                    options_dict) == 1:  # last item in
                options_dict = {}
            elif len(options_dict[
                         str(interaction.guild_id)]) == 1:  # last item in dict
                del options_dict[str(interaction.guild_id)]
            else:
                options_dict[str(interaction.guild_id)].pop(username.casefold())

            # writing to the files
            file_manager.save(f='json/twitterUsers.json',
                              edited_dict=twitter_users_dict)
            file_manager.save(f='json/options.json', edited_dict=options_dict)

            embed = embed_manager.create_embed_header_footer(
                content='No more tweets will be received in this server from '
                        'this user.',
                title='User Unfollowed.',
                icon_url=thumbnails.CHECKMARK_PNG)
            await discord_manager.send(embed=embed, interaction=interaction)

    @nextcord.slash_command(name='unfollow-all',
                            description='Stop receiving all twitter feeds')
    async def unfollow_all(self, interaction: Interaction):
        if not discord_manager.has_permission(interaction):
            await interaction.response.send_message("You are not authorized to "
                                                    "run this command.",
                                                    ephemeral=True)
            return

        twitter_users_dict = file_manager.load('json/twitterUsers.json')
        options_dict = file_manager.load('json/options.json')

        if not twitter_users_dict or str(
                interaction.guild_id) not in options_dict.keys():
            embed = embed_manager.create_embed_header_footer(
                content='Use /follow to receive tweets in this server.',
                title='Not Following Anyone!',
                icon_url=thumbnails.RED_X_PNG)
            await discord_manager.send(embed=embed, interaction=interaction)
            return

        async def no_callback(ctx):
            embed = embed_manager.create_embed_header_footer(
                content='Nothing has been changed.',
                title='Action Cancelled.',
                icon_url=thumbnails.CHECKMARK_PNG)
            await sent_msg.edit(embed=embed, view=no_view)

        async def yes_callback(ctx):
            embed = embed_manager.create_embed_header_footer(
                content='No more tweets will be received in this server.',
                title='Unfollowed all.',
                icon_url=thumbnails.CHECKMARK_PNG)
            await sent_msg.edit(embed=embed, view=no_view)

            for screen_name in twitter_users_dict.keys():
                if str(interaction.guild_id) in twitter_users_dict[screen_name]:
                    twitter_users_dict[screen_name].remove(
                        str(interaction.guild_id))

            to_remove = []
            for screen_name in twitter_users_dict.keys():
                if not twitter_users_dict[screen_name]:
                    to_remove.append(screen_name)

            for screen_name in to_remove:
                del twitter_users_dict[screen_name]

            del options_dict[str(interaction.guild_id)]

            # writing to the files
            file_manager.save(f='json/twitterUsers.json',
                              edited_dict=twitter_users_dict)
            file_manager.save(f='json/options.json', edited_dict=options_dict)

        no_button = Button(label="No", style=ButtonStyle.red)
        yes_button = Button(label="Yes", style=ButtonStyle.green)
        no_button.callback = no_callback
        yes_button.callback = yes_callback

        view = View(timeout=120)
        view.add_item(no_button)
        view.add_item(yes_button)

        no_view = View()

        embed = embed_manager.create_embed_header_footer(
            content='This action cannot be undone.',
            title='Are you sure you want to unfollow everyone?',
            icon_url=thumbnails.QUESTION_MARK_PNG)
        sent_msg = await interaction.send(
            embed=embed,
            view=view,
            ephemeral=True
        )

    @nextcord.slash_command(name='get-follows',
                            description='Lists all followed users')
    async def get_follows(self, interaction: Interaction):
        options_dict = file_manager.load('json/options.json')

        if not str(interaction.guild_id) in options_dict.keys():
            embed = embed_manager.create_embed_header_footer(
                content='Use /follow to receive tweets in this server.',
                title='Not Following Anyone!',
                icon_url=thumbnails.RED_X_PNG)

            await discord_manager.send(embed=embed, interaction=interaction)

        else:

            following = ''

            for user in options_dict[str(interaction.guild_id)].keys():
                following += user + ', '
                if options_dict[str(interaction.guild_id)][user]['ping'] == '0':
                    following += 'No one, '
                elif options_dict[str(interaction.guild_id)][user][
                    'ping'] == '1':
                    following += 'Only Me, '
                else:
                    following += 'Everyone, '

                if options_dict[str(interaction.guild_id)][user][
                    'include_quote_tweets'] == 'False':
                    following += 'No RT\'s\n'
                else:
                    following += 'RT\'s\n'

            embed = embed_manager.create_embed_header_footer(
                content=following,
                title='List of users followed in this server.',
                icon_url=thumbnails.CHECKMARK_PNG,
                footer='To change tweet options, use /unfollow and /follow.')

            await discord_manager.send(embed=embed, interaction=interaction)


def setup(bot):
    bot.add_cog(Twitter(bot))
