import discord
from discord import app_commands
import aiohttp
from credentials import headers
import xml.etree.ElementTree as ET
from .staticfuncs import process_vote, url_holder_region, get_wa_badge, get_things


async def region(interaction, region_name: str):
    region_link = f"https://www.nationstates.net/cgi-bin/api.cgi?region={region_name}"
    founded_url = url_holder_region(region_name, 'foundedtime')
    wa_nations_url = url_holder_region(region_name, 'numwanations')
    ga_vote_url = url_holder_region(region_name, 'gavote')
    sc_vote_url = url_holder_region(region_name, 'scvote')
    wa_badge_url = url_holder_region(region_name, 'wabadges')

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(region_link, headers=headers) as response:
                data = await response.text()
                root = ET.fromstring(data)

                name = root.find('NAME').text
                delegate = root.find('DELEGATE').text
                delegate_wa_votes = root.find('DELEGATEVOTES').text
                nations = root.find('NUMNATIONS').text

                officers = root.findall(".//OFFICER")
                officers_num = len(officers)
                
                power = root.find('POWER').text
                flag = root.find('FLAG').text
                bannerurl = root.find('BANNERURL').text
                banner = f"https://www.nationstates.net/{bannerurl}"
                link = f'https://www.nationstates.net/region={name.replace(" ", "_")}'

                lastmajor = root.find('LASTMAJORUPDATE').text
                lastminor = root.find('LASTMINORUPDATE').text

                founder_element = root.find('FOUNDER')
                if founder_element is not None:
                    founder = founder_element.text
                    if founder != '0':
                        founder = f"[{founder}](https://www.nationstates.net/nation={founder})"
                    else:
                        founder = '`This region has no founder`'
                else:
                    founder = 'No founder information available'

                
                founded_time = ''  # Set a default value for founded_time

                async with session.get(founded_url, headers=headers) as response:
                    data = await response.text()
                    root = ET.fromstring(data)
                    foundedtime_element = root.find('FOUNDEDTIME')

                    if foundedtime_element is not None:
                        foundedtime = foundedtime_element.text
                        if foundedtime != '0':
                            founded_time = f"<t:{foundedtime}:D>"
                        else:
                            founded_time = '`This region was founded in Antiquity`'
                    else:
                        founded_time = 'No founded time information available'
                
                wa_nations = await get_things(session, wa_nations_url, 'NUMUNNATIONS', headers)
                
                try:
                    wa_nations_percent = (int(wa_nations) / int(nations)) * 100

                except ZeroDivisionError:
                    wa_nations_percent = 0


                for_vote_ga, against_vote_ga = await process_vote(session, ga_vote_url, headers, 'GAVOTE', 'FOR', 'AGAINST')
                for_vote_sc, against_vote_sc = await process_vote(session, sc_vote_url, headers, 'SCVOTE', 'FOR', 'AGAINST')
               	type_, res_id_ = await get_wa_badge(session, wa_badge_url, headers)
                res_id_url = f"https://www.nationstates.net/page=WA_past_resolution/id={res_id_}/council=2"

                region_bullet = [
                    ("Delegate", f"[{delegate}](https://www.nationstates.net/nation={delegate})"),
                    ("Regional Officers", f"`{officers_num}`"),
                    ("Nations", f"`{nations}`"),
                    ("Power", f"`{power}`"),
                    ('WA Votes', f"`{delegate_wa_votes}`"),
                    ('WA Nations', f"`{wa_nations} ({wa_nations_percent:.2f}%)`")
                ]

                # Check if res_id_ is not None before including the WA Badges line
                if res_id_ is not None:
                    region_bullet.append(('WA Badges', f"`{type_}ed` by [#SC{res_id_}]({res_id_url})"))

                region_bullet_2 = []
                

                region_bullet_3 = [
                    ('GA Vote', f"For: `{for_vote_ga}`\nAgainst: `{against_vote_ga}`"),
                    ('SC Vote', f"For: `{for_vote_sc}`\nAgainst: `{against_vote_sc}`")
                ]

                region_bullet_4 = [
                    ('Last Major Update', f"<t:{lastmajor}:R>"),
                    ('Last Minor Update', f'<t:{lastminor}:R>')
                ]
                
                if founder != 'No founder information available':
                    region_bullet_2.append(("Founder", founder))
                if founded_time != 'No founded time information available':
                    region_bullet_2.append(("Founded On", founded_time))

                embed = discord.Embed(title=name, url=link)

                for field in region_bullet:
                    embed.add_field(name=field[0], value=field[1], inline=True)

                for field in region_bullet_2:
                    embed.add_field(name=field[0], value=field[1], inline=True)

                for field in region_bullet_3:
                    embed.add_field(name=field[0], value=field[1], inline=True)

                for field in region_bullet_4:
                    embed.add_field(name=field[0], value=field[1], inline=True)
                
                embed.set_thumbnail(url=flag)
                embed.set_image(url=banner)
            
                await interaction.response.send_message(embed=embed)
    except ET.ParseError:
        await interaction.response.send_message('Region does not exist, please check for typos.')


