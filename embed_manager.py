import nextcord
from nextcord import Embed

import file_manager


def create_embed(tweet_title: str,
                 author_name: str,
                 author_url: str,
                 author_icon_url: str,
                 attachment_url: str) -> nextcord.Embed():
    embed = nextcord.Embed(title="",
                           url="",
                           description=tweet_title,
                           color=nextcord.Color.blue())

    embed.set_author(name=author_name,
                     url=author_url,
                     icon_url=author_icon_url)

    if attachment_url:
        embed.set_image(url=attachment_url)
    return embed


def create_setup_embed(page_num=0, inline=False):
    help_dict = file_manager.load('json/setup.json')

    page_num = page_num % len(list(help_dict))
    page_title = list(help_dict)[page_num]
    embed = Embed(title=page_title, color=nextcord.Color.blue())
    for key, val in help_dict[page_title].items():
        if val.startswith('http'):
            embed.add_field(name=key, value='__',
                            inline=inline)
            embed.set_image(val)

        else:
            embed.add_field(name=key, value=val, inline=inline)
            embed.set_footer(
                text=f"Page {page_num + 1} of {len(list(help_dict))}")

    return embed


def create_help_embed(page_num=0, inline=False):
    help_dict = file_manager.load('json/help.json')

    page_num = page_num % len(list(help_dict))
    page_title = list(help_dict)[page_num]
    embed = Embed(title=page_title, color=nextcord.Color.blue())
    for key, val in help_dict[page_title].items():
        embed.add_field(name='`' + key + '`', value=val, inline=inline)
        embed.set_footer(
            text=f"Page {page_num + 1} of {len(list(help_dict))}")
    return embed


def create_embed_header_footer(title: str, content: str,
                               icon_url: str,
                               footer=None) -> nextcord.Embed():
    embed = nextcord.Embed(title="",
                           url="",
                           description=content,
                           color=nextcord.Color.blue())

    embed.set_author(name=title, icon_url=icon_url)

    if not footer:
        embed.set_footer(text="Use /help for more information")
    else:
        embed.set_footer(text=footer)
    return embed


def add_fields(embed: nextcord.Embed, f: str, page_num=0,
               inline=False):
    fields_dict = file_manager.load(f)

    page_num = page_num % len(list(fields_dict))
    page_title = list(fields_dict)[page_num]

    for key, val in fields_dict[page_title].items():
        embed.add_field(name=key, value=val, inline=inline)
    return embed
