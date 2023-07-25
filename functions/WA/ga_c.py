import discord
import aiohttp
from discord import app_commands
import xml.etree.ElementTree as ET
from credentials import headers

async def ga(interaction, proposal_id: int):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://www.nationstates.net/cgi-bin/api.cgi?wa=1&id={proposal_id}&q=resolution', headers=headers) as response:
                data = await response.text()
                root = ET.fromstring(data)
                
                resolution = root.find('RESOLUTION')

                name = resolution.find('NAME').text
                category = resolution.find('CATEGORY').text
                date_passed = resolution.find('IMPLEMENTED').text
                for_votes = resolution.find('TOTAL_VOTES_FOR').text
                against_votes = resolution.find('TOTAL_VOTES_AGAINST').text
                created = resolution.find('CREATED').text
                author = resolution.find('PROPOSED_BY').text

                link = f"https://www.nationstates.net/page=WA_past_resolution/id={proposal_id}/council=1"
                author_nation_link = f"https://www.nationstates.net/nation={author}"
    except:
        await interaction.response.send_message('Resolution not found, try again.')

    bullet = [
        f"- Category: `{category}`",
        f"- Author: [{author}]({author_nation_link})",
        f"- Created on: <t:{created}:F>"
    ]

    ga_embed = [
        ('Date Passed', f"<t:{date_passed}:F>"),
        ('For', f"`{for_votes}`"),
        ('Against', f"`{against_votes}`")
    ]

    ga_bullet = '\n'.join(bullet)
    embed = discord.Embed(title=name, url=link)
    embed.add_field(name='\u200b', value=ga_bullet, inline=False)

    for field in ga_embed:
        embed.add_field(name=field[0], value=field[1], inline=True)

    embed.set_thumbnail(url="https://www.nationstates.net/images/ga.jpg")
    await interaction.response.send_message(embed=embed)


    embed = discord.Embed(title=res, url=link)
    embed.add_field(name="Date of Implementation", value=formatted_date)
    embed.add_field(name = 'Author', value=f"https://www.nationstates.net/nation={author}")
    await interaction.response.send_message(embed=embed)
