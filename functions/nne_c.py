import discord
from discord import app_commands
from discord.ui import Button
import aiohttp
import re
from credentials import headers


async def nations_not_endorsing(interaction, nation_name: str, region_name: str, message: str):
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
        await interaction.response.send_message("Endorsements not found in the data.")
        return
    
    unnations = re.search(r"<UNNATIONS>(.*?)</UNNATIONS>", region_wa, re.DOTALL)
    if unnations:
        extracted_data_region = unnations.group(1)
        unnations_list = extracted_data_region.split(',')
    else:
        await interaction.response.send_message("UNNATIONS not found in the data.")
        return
    
    nne = list(set(unnations_list) - set(endorsements_list))
    
    with open("sent_nations.txt", "r+") as file:
        sent_nations = file.read().splitlines()

        if not sent_nations:
            sent_nations = []

        new_nations = [nation for nation in nne if nation not in sent_nations]

        if not new_nations:
            await interaction.response.send_message("All nations have been sent.")
            return

        chunk_size = 8
        chunk = new_nations[:chunk_size]
        sent_nations += chunk
        file.seek(0)
        file.write("\n".join(sent_nations))
        file.truncate()

        embed = discord.Embed(title="Nations Not Endorsing", color=0x00ff00)
        nation_list = ", ".join(chunk)
        embed.add_field(name="Nations", value=nation_list, inline=True)

        view = discord.ui.View()

        # Generate individual URLs for each nation
        for nation in chunk:
            url = f"https://www.nationstates.net/page=compose_telegram?tgto={nation}&message={message}"
            button = discord.ui.Button(style=discord.ButtonStyle.link, label='Open Telegram', url=url)
            view.add_item(button)

        embed.set_footer(text='Open Telegram')
        await interaction.response.send_message(embed=embed, view=view)


