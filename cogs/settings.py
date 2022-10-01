import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

import discord_manager
import embed_manager
import settings_controller
import thumbnails


class Settings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='settings',
                            description='Lists all bot settings')
    async def settings(self, interaction: Interaction):
        # check permissions
        if not discord_manager.has_permission(interaction):
            await interaction.response.send_message("You are not authorized to "
                                                    "run this command.",
                                                    ephemeral=True)
            return

        # initializing default settings if guild not in database
        if not settings_controller.in_settings(str(interaction.guild_id)):
            settings_controller.add_default(str(interaction.guild_id))

        embed = embed_manager.create_embed_header_footer(
            title='Settings',
            content='Bot settings can be changed by clicking on the '
                    'corresponding options below.\nChange settings by running '
                    '/setting',
            icon_url=thumbnails.BOT_ICON
        )
        embed.add_field(
            name='Adapt profile picture ~ ' + settings_controller.fetch_setting(
                str(interaction.guild_id), 'Adapt profile picture'),
            value='Profile picture of sent messages will change according to '
                  'the profile picture of the tweeting user. '
        )
        await discord_manager.send(
            embed=embed,
            interaction=interaction,
            ephemeral=True
        )

    @nextcord.slash_command(name='setting',
                            description='Changes the bots settings')
    async def setting(
            self,
            interaction: Interaction,
            setting: str = SlashOption(
                required=True,
                description='Name of the setting to change',
                choices={a: a for a in settings_controller.get_all_settings()}
            ),
    ):
        # check permissions
        if not discord_manager.has_permission(interaction):
            await interaction.response.send_message("You are not authorized to "
                                                    "run this command.",
                                                    ephemeral=True)
            return

        if not settings_controller.in_settings(str(interaction.guild_id)):
            settings_controller.add_default(str(interaction.guild_id))

        current_setting = settings_controller.fetch_setting(
            str(interaction.guild_id), setting)
        if current_setting == 'On':
            settings_controller.change_setting_controller(
                str(interaction.guild_id),
                setting, 'Off')
            embed = embed_manager.create_embed_header_footer(
                title='Setting successfully changed.',
                content='Adapt profile picture is now set to OFF',
                icon_url=thumbnails.CHECKMARK_PNG
            )
            await discord_manager.send(
                embed=embed,
                interaction=interaction,
                ephemeral=True
            )

        elif current_setting == 'Off':
            settings_controller.change_setting_controller(
                str(interaction.guild_id),
                setting, 'On')
            embed = embed_manager.create_embed_header_footer(
                title='Setting successfully changed.',
                content='Adapt profile picture is now set to ON',
                icon_url=thumbnails.CHECKMARK_PNG
            )
            await discord_manager.send(
                embed=embed,
                interaction=interaction,
                ephemeral=True
            )
        else:
            print('Not in settings')


def setup(bot):
    bot.add_cog(Settings(bot))
