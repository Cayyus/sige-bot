import discord
from discord import app_commands
import aiohttp
import re
from credentials import headers

async def wa_nations(interaction, region_name: str):
    region_wa_nations = f"https://www.nationstates.net/cgi-bin/api.cgi?region={region_name}&q=wanations"
    async with aiohttp.ClientSession() as session:
        async with session.get(region_wa_nations, headers=headers) as wa_response:
            region_wa_data = await wa_response.text()
            
            region_wa = re.search(r"<UNNATIONS>(.*?)</UNNATIONS>", region_wa_data, re.DOTALL)
            if region_wa:
                wa_nations = region_wa.group(1)
                wa_list = wa_nations.split(',')

                with open('region_wa_nations.txt', 'a+') as file:
                    file.seek(0)
                    existing_nations = file.read().splitlines()
                    new_nations = [nation for nation in wa_list if nation not in existing_nations][:10]

                    if new_nations:
                        embed = discord.Embed()
                        nations_string = '\n'.join(f"[{nation}](https://www.nationstates.net/nation={nation}#composebutton)" for nation in new_nations)
                        embed.add_field(name = 'WA Nations', value=nations_string, inline=False)
                        
                        for nation in new_nations:
                            if nation not in existing_nations:
                                file.write(nation + '\n')

                        await interaction.response.send_message(embed=embed)


