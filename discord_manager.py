from typing import Union

import aiohttp
import nextcord
from nextcord.errors import NotFound

import file_manager
import settings_controller
import thumbnails


async def send(embed, interaction, ephemeral=True, view=None):
    while True:
        try:
            if view:
                await interaction.send(embed=embed, ephemeral=ephemeral,
                                       view=view)
            else:
                await interaction.send(embed=embed, ephemeral=ephemeral)
        except NotFound:
            continue
        else:
            break


def get_webhook(guild_id: str) -> Union[str, None]:
    webhooks_dict = file_manager.load('json/webhooks.json')
    if guild_id in webhooks_dict.keys():
        return webhooks_dict[guild_id]
    return None


def has_permission(interaction):
    if interaction.user.id == 544266747067236358:
        return True
    if not interaction.user.guild_permissions.administrator:
        return False
    return True


def get_ping(guild_id, screen_name):
    options_dict = file_manager.load('json/options.json')
    to_ping = ''

    if options_dict[str(guild_id)][screen_name]['ping'] == '1':
        to_ping = options_dict[str(guild_id)][screen_name]['ping_user']

    elif options_dict[str(guild_id)][screen_name]['ping'] == '2':
        to_ping = '@everyone'
    return to_ping


async def send_webhook(embed, avatar_url, guild_id, screen_name,
                       to_ping,
                       webhooks_dict):
    if not settings_controller.in_settings(str(guild_id)):
        settings_controller.add_default(str(guild_id))

    # Adapt profile pic setting
    settings_dict = file_manager.load('json/settings.json')
    if settings_dict[str(guild_id)]['Adapt profile picture'] == 'Off':
        avatar_url = thumbnails.BOT_ICON

    async with aiohttp.ClientSession() as session:
        try:
            url = webhooks_dict[guild_id]
        except KeyError:
            pass
        else:
            webhook = nextcord.Webhook.from_url(url=url,
                                                session=session)
            await webhook.send(f'{to_ping}',
                               embed=embed,
                               username=f'{screen_name} ~ UTBG Bot ',
                               avatar_url=avatar_url)
