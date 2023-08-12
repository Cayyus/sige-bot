import discord
from discord import app_commands
import aiohttp
import asyncio
from credentials import headers
from discord.utils import get

async def verify(interaction, nation: str, client):
    await interaction.response.send_message('Please check your DMs for instructions.')
    user = interaction.user
    await user.send('Please visit https://www.nationstates.net/page=verify_login on your verification nation and copy paste the code below.')

    def check(m):
        return m.author == user and isinstance(m.channel, discord.DMChannel)
    
    try:
        response = await client.wait_for('message', check=check, timeout=60)
        code = response.content

    except asyncio.TimeoutError:
        await user.send('Sorry, you took too long to respond. Please try again.')

    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://www.nationstates.net/cgi-bin/api.cgi?a=verify&nation={nation}&checksum={code}', headers=headers) as response:
            data = await response.text()
            data = data.strip()

            if data == '1':
                await interaction.followup.send(f'Your nation has been verified.')
                guild = interaction.guild
                role = 'Registered'
                registered_role = get(guild.roles, name=role)
                await user.add_roles(registered_role)
            else:
                await interaction.followup.send('Nation verification failed.')
