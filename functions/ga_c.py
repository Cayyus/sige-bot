import discord
import aiohttp
from discord import app_commands
import xml.etree.ElementTree as ET
from credentials import headers

async def ga(interaction, proposal_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://www.nationstates.net/cgi-bin/api.cgi?wa=1&id={proposal_id}&q=resolution', headers=headers) as response:
            data = await response.text()
            root = ET.fromstring(data)

            res_element = root.find("RESOLUTION")
            if res_element is None:
                
                await interaction.response.send_message("Unable to retrieve resolution information.")
                return

            name_element = res_element.find("NAME")
            if name_element is None:
                
                await interaction.response.send_message("Unable to retrieve resolution name.")
                return

            res = name_element.text

            date_element = res_element.find("IMPLEMENTED")
            if date_element is None:
                
                await interaction.response.send_message("Unable to retrieve implementation date.")
                return
            
            author_element = res_element.find("PROPOSED_BY")
            if date_element is None:
                
                await interaction.response.send_message("Unable to retrieve author.")
                return

            author = author_element.text
            
            date = date_element.text
            formatted_date = f"<t:{date}:R>"

            link = f"https://www.nationstates.net/page=WA_past_resolution/id={proposal_id}/council=1"

    embed = discord.Embed(title=res, url=link)
    embed.add_field(name="Date of Implementation", value=formatted_date)
    embed.add_field(name = 'Author', value=f"https://www.nationstates.net/nation={author}")
    await interaction.response.send_message(embed=embed)