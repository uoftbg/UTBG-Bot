import aiohttp
import nextcord
from nextcord import Interaction, InvalidArgument, SlashOption
from nextcord.errors import HTTPException
from nextcord.ext import commands

import discord_manager
import embed_manager
import file_manager
import thumbnails


class Webhooks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='set-webhook',
                            description='Sets the link of the webhook')
    async def set_webhook(self, interaction: Interaction,
                          link: str = SlashOption(
                              required=True,
                              description='The link of the webhook')):
        if not discord_manager.has_permission(interaction):
            await interaction.response.send_message("You are not authorized to "
                                                    "run this command.",
                                                    ephemeral=True)
            return
        # verifying webhook
        async with aiohttp.ClientSession() as session:
            try:
                webhook = nextcord.Webhook.from_url(url=link, session=session)
                full_webhook = await webhook.fetch()
            except (InvalidArgument, HTTPException):
                embed = embed_manager.create_embed_header_footer(
                    content='Please check the URL is correct and try again.',
                    title='Invalid Webhook URL!',
                    icon_url=thumbnails.RED_X_PNG)
                await discord_manager.send(embed=embed, interaction=interaction)

            else:
                # checking if the webhook is from the same guild
                if not full_webhook.guild_id == interaction.guild_id:
                    embed = embed_manager.create_embed_header_footer(
                        content='Please check the URL is correct and try again.',
                        title='Webhook URL not from this server!',
                        icon_url=thumbnails.RED_X_PNG)
                    await discord_manager.send(embed=embed,
                                               interaction=interaction)
                    return

                # saving the webhook
                webhooks_dict = file_manager.load('json/webhooks.json')
                webhooks_dict[str(interaction.guild_id)] = link
                file_manager.save(f='json/webhooks.json', edited_dict=webhooks_dict)

                embed = embed_manager.create_embed_header_footer(
                    content='The channel connected the to webhook will '
                            'receive tweet notifications!',
                    title='Webhook successfully set!',
                    icon_url=thumbnails.CHECKMARK_PNG)
                await discord_manager.send(embed=embed, interaction=interaction)

    @nextcord.slash_command(name='remove-webhook',
                            description='Removes the link of the webhook')
    async def remove_webhook(self,
                             interaction: Interaction,
                             link: str = SlashOption(
                                 required=True,
                                 description='The link of the webhook')):
        if not discord_manager.has_permission(interaction):
            await interaction.response.send_message("You are not authorized to "
                                                    "run this command.",
                                                    ephemeral=True)
            return

        # verifying webhook
        webhooks_dict = file_manager.load('json/webhooks.json')

        # webhooks match
        if webhooks_dict[str(str(interaction.guild_id))] == link:
            del webhooks_dict[str(interaction.guild_id)]
            file_manager.save(f='json/webhooks.json', edited_dict=webhooks_dict)

            embed = embed_manager.create_embed_header_footer(
                content='The channel connected the to webhook will '
                        'stop receiving tweet notifications!',
                title='Webhook removed successfully!',
                icon_url=thumbnails.CHECKMARK_PNG)
            await discord_manager.send(embed=embed, interaction=interaction)
        else:
            embed = embed_manager.create_embed_header_footer(
                content='Please check the URL is correct and try again.',
                title='Invalid Webhook URL!',
                icon_url=thumbnails.RED_X_PNG)
            await discord_manager.send(embed=embed, interaction=interaction)


def setup(bot):
    bot.add_cog(Webhooks(bot))
