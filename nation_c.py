import discord
from discord import app_commands
import xml.etree.ElementTree as ET
import aiohttp
from credentials import headers

async def nation(interaction, nation_name: str):
    async with aiohttp.ClientSession() as session:
            async with session.get(f'https://www.nationstates.net/cgi-bin/api.cgi?nation={nation_name}', headers=headers) as response:
                data = await response.text()
                root = ET.fromstring(data)
                type_nation = root.find("TYPE").text
                nation_name = f"The {type_nation} of {nation_name}"
                name = root.find("NAME").text
                region = root.find("REGION").text
                founded = root.find("FIRSTLOGIN").text
                flag = root.find("FLAG").text
                endorsed_by = root.find("ENDORSEMENTS").text
                wa_status = root.find('UNSTATUS').text
                category = root.find('CATEGORY').text
                if endorsed_by is None:
                    endorsements = None
                else:
                    endorsements = len(endorsed_by.split(','))
                link = f'https://www.nationstates.net/nation={name.replace(" ", "_")}'
                region_link = f'https://www.nationstates.net/region={region.replace(" ", "_")}'

                nation_embed_points = [
                    f"- `Founded`: <t:{founded}:D>",
                    f"- `Classification: {category}`",
                    f"- `WA Status: {wa_status}`",
                    f"- `Endorsements: {endorsements}`"
                ]

    nation_embed = "\n".join(nation_embed_points)
    embed = discord.Embed(title=nation_name, url=link, color=0x00ff00)
    embed.add_field(name='General Information', value=nation_embed, inline=False)
    embed.add_field(name='Region', value=f"[{region}]({region_link})")
    embed.set_thumbnail(url=flag)
    await interaction.response.send_message(embed=embed)
