import nextcord
from nextcord import ButtonStyle, Interaction
from nextcord.ext import commands
from nextcord.ui import Button, View

import discord_manager
import embed_manager
import thumbnails


class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='setup',
                            description='Walks through the features and '
                                        'setup of the bot')
    async def setup(self, interaction: Interaction):
        current_page = 0

        # callbacks for button presses
        async def next_callback(ctx):
            nonlocal current_page, sent_msg
            current_page += 1
            await sent_msg.edit(
                embed=embed_manager.create_setup_embed(page_num=current_page),
                view=view
            )

        async def previous_callback(ctx):
            nonlocal current_page, sent_msg
            current_page -= 1
            await sent_msg.edit(
                embed=embed_manager.create_setup_embed(page_num=current_page),
                view=view
            )

        # add buttons to embed
        previous_button = Button(label="<", style=ButtonStyle.blurple)
        next_button = Button(label=">", style=ButtonStyle.blurple)
        previous_button.callback = previous_callback
        next_button.callback = next_callback

        view = View(timeout=120)
        view.add_item(previous_button)
        view.add_item(next_button)

        sent_msg = await interaction.send(
            embed=embed_manager.create_setup_embed(),
            view=view,
            ephemeral=True
        )

    @nextcord.slash_command(name='invite',
                            description='Invite this bot to your own server')
    async def invite(self, interaction: Interaction):
        embed = embed_manager.create_embed_header_footer(
            content='You can invite this bot to your own server by clicking '
                    'the button below!\n Alternatively, you can click the bot '
                    'profile, then "Add to Server."',
            title='Want UTBG Bot in your own server?',
            icon_url=thumbnails.BOT_ICON)

        link_button = Button(label="Add to Server", style=ButtonStyle.blurple,
                             url=thumbnails.INVITE_LINK)
        view = View(timeout=120)
        view.add_item(link_button)

        await discord_manager.send(
            embed=embed,
            interaction=interaction,
            ephemeral=False,
            view=view
        )

    @nextcord.slash_command(name='info',
                            description='Learn more about this bot')
    async def info(self, interaction: Interaction):
        embed = embed_manager.create_embed_header_footer(
            content='UTBG Bot is Discord Bot which allows you to get realtime '
                    'tweet notifications in your server. More features and other '
                    'apps (including instagram) are coming in the near future!',
            title='About UTBG Bot',
            icon_url=thumbnails.BOT_ICON
        )
        embed_manager.add_fields(embed=embed, f='json/info.json')
        await discord_manager.send(
            embed=embed,
            interaction=interaction,
            ephemeral=False
        )

    @nextcord.slash_command(name='help',
                            description='Get the list of available commands')
    async def help(self, interaction: Interaction):
        current_page = 0

        # callbacks for button presses
        async def next_callback(ctx):
            nonlocal current_page, sent_msg
            current_page += 1
            await sent_msg.edit(
                embed=embed_manager.create_help_embed(page_num=current_page),
                view=view)

        async def previous_callback(ctx):
            nonlocal current_page, sent_msg
            current_page -= 1
            await sent_msg.edit(
                embed=embed_manager.create_help_embed(page_num=current_page),
                view=view)

        # add buttons to embed
        previous_button = Button(label="<", style=ButtonStyle.blurple)
        next_button = Button(label=">", style=ButtonStyle.blurple)
        previous_button.callback = previous_callback
        next_button.callback = next_callback

        view = View(timeout=120)
        view.add_item(previous_button)
        view.add_item(next_button)

        sent_msg = await interaction.send(
            embed=embed_manager.create_help_embed(current_page),
            view=view,
            ephemeral=False
        )

    @nextcord.slash_command(name='ping', description='Tests bots latency')
    async def ping(self, interaction: Interaction):
        embed = embed_manager.create_embed_header_footer(
            content=f'Latency: {round(self.bot.latency * 1000, ndigits=1)} ms',
            title='Pong!',
            icon_url=thumbnails.BOT_ICON)

        await discord_manager.send(embed=embed, interaction=interaction)


def setup(bot):
    bot.add_cog(Commands(bot))
