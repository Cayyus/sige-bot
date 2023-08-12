import discord
from discord import app_commands

async def help(interaction):
    commands_list = [
        '- **help - shows this command**',
        '- **nation (nation name) - Gives information about a NationStates nation**',
        '- **region (region name) - Gives information about a NationStates region**',
        '- **ga (proposal id) - Gives information about a proposal already passed in the GA**',
        '- **sc (proposal id) - Gives information about a proposal already passed in the SC**',
        '- **dispatch (dispatch id) - Gives information about a dispatch**', 
        '- **verify (nation name) - Verifies a nation to a specific user**'
    ]
    commands_list = '\n'.join(commands_list)

    embed = discord.Embed(title = 'List of Commands')
    embed.add_field(name ='\u200b', value=commands_list, inline=False)
    await interaction.response.send_message(embed=embed)
