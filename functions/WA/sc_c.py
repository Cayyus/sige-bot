import discord
import aiohttp
from discord import app_commands
import xml.etree.ElementTree as ET
from credentials import headers


async def sc(interaction, proposal_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://www.nationstates.net/cgi-bin/api.cgi?wa=2&id={proposal_id}&q=resolution', headers=headers) as response:
            data = await response.text()
            root = ET.fromstring(data)

            res_element = root.find("RESOLUTION")
            name = res_element.find("NAME").text
            author = res_element.find("PROPOSED_BY").text
            implemented = res_element.find("IMPLEMENTED").text
            forvotes = res_element.find('TOTAL_VOTES_FOR').text
            againstvotes = res_element.find("TOTAL_VOTES_AGAINST").text
            link = f"https://www.nationstates.net/page=WA_past_resolution/id={proposal_id}/council=2"
            author_nation_link = f"https://www.nationstates.net/nation={author}"
            _id = res_element.find('COUNCILID').text


            bullets = [
                    f"- Author: [{author}]({author_nation_link})",
                    f"- Date of Passing: <t:{implemented}:R>",
                    f"- For: `{forvotes}`",
                    f"- Against: `{againstvotes}`"
                    ]
        bullet_embed = '\n'.join(bullets)
        embed = discord.Embed(title=name, url=link)
        embed.add_field(name=f'Information about SC#{_id}', value=bullet_embed, inline=False)
        await interaction.response.send_message(embed=embed)
