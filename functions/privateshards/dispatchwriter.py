import discord
from discord import app_commands
import aiohttp
import re
from credentials import headers

async def dispatch_write(interaction, title: str, body:str):
    with open('dispatch_nation.txt', 'r') as file:
        lines = file.readlines()

        nation_name = None
        nation_password = None

        for line in lines:
            if line.startswith('Nation Name'):
                nation_name = line.split('_')[-1].strip().split(' - ')[0]
            elif line.startswith('Nation Password'):
                nation_password = line.split('_')[-1].strip().split(' - ')[-1]

    if nation_name is None or nation_password is None:
        await interaction.response.send_message("Nation name or password not found.")
        return
    
    NATION_NAME = nation_name
    NATION_PASSWORD = nation_password

    url = "https://www.nationstates.net/cgi-bin/api.cgi"
    pre_headers = {"X-Password": NATION_PASSWORD, 
            "User-Agent": headers['User-Agent']}

    pre_params = {"nation": NATION_NAME, 
            "c": 'dispatch', 
            'dispatch': 'add', 
            'title': title, 
            'text': body, 
            'category': '3', 
            'subcategory': '315', 
            'mode': 'prepare'}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=pre_headers, params=pre_params) as response:
            response_text = await response.text()
            x_pin = response.headers.get('X-Pin')

            token_match = re.search(r"<SUCCESS>(.*?)</SUCCESS>", response_text, re.DOTALL)
            if token_match:
                token = token_match.group(1)
            else:
                await interaction.response.send_message("Failed to retrieve token.")
                return

    execute_headers = {"X-Pin": x_pin, 
                    "X-Password": NATION_PASSWORD, 
                    "User-Agent": headers['User-Agent']}
    execute_params = {"nation": NATION_NAME, 
                    "c": 'dispatch', 
                    'dispatch': 'add', 
                    'title': title, 
                    'text': body, 
                    'category': '3', 
                    'subcategory': '315', 
                    'mode': 'execute', 
                    'token': token}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=execute_headers, params=execute_params) as response:
            await interaction.response.send_message("Dispatch successfully sent.")
