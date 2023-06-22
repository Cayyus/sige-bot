import discord
from discord import app_commands

async def nation_register(interaction, nation_name: str, nation_password: str):
    with open('dispatch_nation.txt', 'w') as file:
        file.write(f'Nation Name_{nation_name} - {nation_name}\n' + f"Nation Password_{nation_name} - {nation_password}")
        await interaction.response.send_message("Nation Registered!")
    
