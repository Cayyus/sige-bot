import discord
from discord import app_commands
import aiohttp
import re
from credentials import headers

async def nations_not_endorsing(interaction, nation_name: str, region_name: str):
    url_endo = f"https://www.nationstates.net/cgi-bin/api.cgi?nation={nation_name}&q=endorsements"
    url_region_wa = f"https://www.nationstates.net/cgi-bin/api.cgi?region={region_name}&q=wanations"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url_endo, headers=headers) as response_endo:
            endo_data = await response_endo.text()
        
        async with session.get(url_region_wa, headers=headers) as response_endo_wa:
            region_wa = await response_endo_wa.text()

    endorsements = re.search(r"<ENDORSEMENTS>(.*?)</ENDORSEMENTS>", endo_data, re.DOTALL)
    if endorsements:
        extracted_data = endorsements.group(1)
        endorsements_list = extracted_data.split(',')
    else:
        await interaction.response.send_message("Endorsements not found in the XML data.")
        return
    
    unnations = re.search(r"<UNNATIONS>(.*?)</UNNATIONS>", region_wa, re.DOTALL)
    if unnations:
        extracted_data_region = unnations.group(1)
        unnations_list = extracted_data_region.split(',')
    else:
        await interaction.response.send_message("UNNATIONS not found in the XML data.")
        return
    
    unnations_only = list(set(unnations_list) - set(endorsements_list))
    
    nations_per_string = 8
    unnations_strings = [', '.join(unnations_only[i:i+nations_per_string]) for i in range(0, len(unnations_only), nations_per_string)]
    
    response_message = f"Nations Not Endorsing {nation_name}:\n"
    for i, string in enumerate(unnations_strings, 1):
        response_message += f"String {i}: {string}\n"
    
    
    messages = []
    current_message = ""
    for line in response_message.splitlines():
        if len(current_message) + len(line) > 2000:
            messages.append(current_message)
            current_message = ""
        current_message += line + "\n"
    messages.append(current_message)
    
    # Send the messages
    for i, message in enumerate(messages):
        if i == 0:
            await interaction.response.send_message(message)
        else:
            await interaction.followup.send(message)


