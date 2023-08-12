import discord
from discord import app_commands
import xml.etree.ElementTree as ET
import aiohttp
from credentials import headers
from .staticfuncs import url_holder_nation, get_things

icons = [':notebook:', ':watch:', ':blue_book:']

async def nation(interaction, nation_name: str):
    bannerurl = url_holder_nation(nation_name, 'banner')
    ga_vote_url = url_holder_nation(nation_name, 'gavote')
    sc_vote_url = url_holder_nation(nation_name, 'scvote')
    try:
        async with aiohttp.ClientSession() as session:
                async with session.get(f'https://www.nationstates.net/cgi-bin/api.cgi?nation={nation_name}', headers=headers) as response:
                    data = await response.text()
                    root = ET.fromstring(data)

                    fullname = root.find('FULLNAME').text

                    _name = root.find('NAME').text

                    region = root.find("REGION").text
                    founded = root.find("FIRSTLOGIN").text
                    flag = root.find("FLAG").text

                    endorsed_by = root.find("ENDORSEMENTS").text
                    wa = root.find('UNSTATUS').text
                    category = root.find('CATEGORY').text
                    last_activity = root.find('LASTLOGIN').text

                    issues_answered = root.find('ISSUES_ANSWERED').text
                    factbooks = root.find('FACTBOOKS').text
                    dispatches = root.find('DISPATCHES').text

                    population = root.find('POPULATION').text

                    banner_ = await get_things(session, bannerurl, 'BANNER', headers)
                    banner = f"https://www.nationstates.net/images/banners/{banner_}.jpg"
                    

                    ga_vote = await get_things(session, ga_vote_url, 'GAVOTE', headers)
                    sc_vote = await get_things(session, sc_vote_url, 'SCVOTE', headers)

                    try:
                        number = int(population)
                        if number >= 1000:
                            billion = number / 1000
                            population = f"{billion} Billion"
                        else:
                            population = f"{population} Million"
                    except ValueError:
                        pass

                    if endorsed_by is None:
                        endorsements = None
                    else:
                        endorsements = len(endorsed_by.split(','))
                    
                    link = f'https://www.nationstates.net/nation={_name.replace(" ", "_")}'
                    region_link = f'https://www.nationstates.net/region={region.replace(" ", "_")}'
                    factbook_link = f'https://www.nationstates.net/nation={_name.replace(" ", "_")}/detail=factbook'

        nation_embed = [
            (f'{icons[1]}Founded', f"<t:{founded}:F>"),
            ('Category', f"`{category}`"),
            ('Region', f"[{region}]({region_link})"),
            ('WA Status', f"`{wa}`"),
            ('Endorsements', f"`{endorsements}`"),
            ('Population', f'`{population}`'),
            ('Issues Answered', f'`{issues_answered}`'),
            ('GA Vote', f'`{ga_vote}`'),
            ('SC Vote', f"`{sc_vote}`"),
            (f'{icons[0]}Factbooks', f'[{factbooks}]({factbook_link})'),
            (f'{icons[2]}Dispatches', f'`{dispatches}`'),
            ('Last Seen', f"<t:{last_activity}:R>")
        ]

        embed = discord.Embed(title=fullname, url=link, color=0x00ff00)
        for field in nation_embed:
            embed.add_field(name=field[0], value=field[1], inline=True)

        embed.set_thumbnail(url=flag)
        embed.set_image(url=banner)
        await interaction.response.send_message(embed=embed)
    except:
        await interaction.response.send_message('Nation does not exist, please check for typos.')
