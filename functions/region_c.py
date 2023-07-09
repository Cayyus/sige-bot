import discord
from discord import app_commands
import aiohttp
import re
from credentials import headers
import xml.etree.ElementTree as ET


def url_holder(region_name, query):
    return f"https://www.nationstates.net/cgi-bin/api.cgi?region={region_name}&q={query}"

async def region(interaction, region_name: str):
    region_link = f"https://www.nationstates.net/cgi-bin/api.cgi?region={region_name}"
    founded_url = url_holder(region_name, 'foundedtime')
    wa_nations_url = url_holder(region_name, 'numwanations')
    ga_vote_url = url_holder(region_name, 'gavote')
    sc_vote_url = url_holder(region_name, 'scvote') 

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
            link = f'https://www.nationstates.net/region={name.replace(" ", "_")}'

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
            
            async with session.get(wa_nations_url, headers=headers) as response:
                data = await response.text()
                root = ET.fromstring(data)
                wa_nations = root.find('NUMUNNATIONS').text
            
            try:
                wa_nations_percent = (int(wa_nations) / int(nations)) * 100

            except ZeroDivisionError:
                wa_nations_percent = 0

            async def process_vote(session, url, headers, parent_element, for_element, against_element):
                async with session.get(url, headers=headers) as response:
                    data = await response.text()
                    root = ET.fromstring(data)
                    vote_parent_element = root.find(parent_element)
                    for_element = vote_parent_element.find(for_element)
                    against_element = vote_parent_element.find(against_element)

                    if for_element is not None:
                        for_vote = for_element.text
                    else:
                        for_vote = 'N/A'
                    if against_element is not None:
                        against_vote = against_element.text
                    else:
                        against_vote = 'N/A'

                    return for_vote, against_vote

            for_vote_ga, against_vote_ga = await process_vote(session, ga_vote_url, headers, 'GAVOTE', 'FOR', 'AGAINST')
            for_vote_sc, against_vote_sc = await process_vote(session, sc_vote_url, headers, 'SCVOTE', 'FOR', 'AGAINST')

                
            region_bullet = [
                ("Delegate", f"[{delegate}](https://www.nationstates.net/nation={delegate})"),
                ("Regional Officers", f"`{officers_num}`"),
                ("Nations", f"`{nations}`"),
                ("Power", f"`{power}`"),
                ('WA Votes', f"`{delegate_wa_votes}`"),
                ('WA Nations', f"`{wa_nations} ({wa_nations_percent:.2f}%)`")
            ]

            region_bullet_2 = []
            

            region_bullet_3 = [
                ('GA Vote', f"For`{for_vote_ga}`\nAgainst`{against_vote_ga}`"),
                ('SC Vote', f"For`{for_vote_sc}`\nAgainst`{against_vote_sc}`")
            ]
            
            if founder != 'No founder information available':
                region_bullet_2.append(("Founder", founder))
            if founded_time != 'No founded time information available':
                region_bullet_2.append(("Founded On", founded_time))

            embed = discord.Embed(title=name, url=link)

            for field in region_bullet:
                embed.add_field(name=field[0], value=field[1], inline=True)

            embed.add_field(name='\u200b', value='\n', inline=False)

            for field in region_bullet_2:
                embed.add_field(name=field[0], value=field[1], inline=True)

            embed.add_field(name='\u200b', value='\n', inline=False)

            for field in region_bullet_3:
                embed.add_field(name=field[0], value=field[1], inline=True)

            embed.set_thumbnail(url=flag)
        
            await interaction.response.send_message(embed=embed)


