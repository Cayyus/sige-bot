import aiohttp
import xml.etree.ElementTree as ET
import discord
from discord import app_commands
from credentials import headers

async def dispatch(interaction, dispatch_link: str):
    dispatch_split = dispatch_link.split('id=')
    dispatch_id = dispatch_split[1]
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://www.nationstates.net/cgi-bin/api.cgi?q=dispatch;dispatchid={dispatch_id}', headers=headers) as response:
                data = await response.text()
                root = ET.fromstring(data)

                dispatch = root.find("DISPATCH")
                if dispatch is None:
                    return
                    
                title_ele = dispatch.find("TITLE")
                if title_ele is None:
                    return
                    
                title = title_ele.text

                author_ele = dispatch.find("AUTHOR")
                if author_ele is None:
                    return

                author = author_ele.text
                author_link = f"https://www.nationstates.net/nation={author}"

                creation_date_ele = dispatch.find("CREATED")
                if creation_date_ele is None:
                    return
                    
                creation_date = creation_date_ele.text

                views_ele = dispatch.find("VIEWS")
                if views_ele is None:
                    return
                    
                views = views_ele.text

                score_ele = dispatch.find("SCORE")
                if score_ele is None:
                    return
                    
                scores = score_ele.text

                link = f"https://www.nationstates.net/page=dispatch/id={dispatch_id}"

            dispatch_bullet = [
                f"- `Author`: [{author}]({author_link})",
                f"- `Date Created`: <t:{creation_date}:D>",
                f"- `Views`: {views}",
                f"- `Score`: {scores}"
            ]

            dispatch_bullet_embed = "\n".join(dispatch_bullet)
            embed = discord.Embed(title=title, url=link)
            embed.add_field(name='General Information', value=dispatch_bullet_embed, inline=False)
            await interaction.response.send_message(embed=embed)
    except:
        await interaction.response.send_message('Dispatch not found, please try again.')
