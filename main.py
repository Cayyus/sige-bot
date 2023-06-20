import discord
from discord import app_commands
from credentials import TOKEN
from functions.dispatch_c import dispatch
from functions.ga_c import ga
from functions.nation_c import nation
from functions.nne_c import nations_not_endorsing

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await client.wait_until_ready()
    print(f"We have logged in as {client.user}")
    await tree.sync()

@tree.command(name = 'nation', description='Sends information about a particular nation')
async def nation_command(interaction, nation_name: str):
    await nation(interaction, nation_name)

@tree.command(name='ga', description='To see information about the General Assembly')
async def ga_command(interaction, proposal_id: int):
    await ga(interaction, proposal_id)

@tree.command(name='dispatch', description='To see information about a dispatch')
async def dispatch_command(interaction, dispatch_link: str):
    await dispatch(interaction, dispatch_link)

@tree.command(name = 'nne', description='Nations Not Endorsing (NNE), generates a list of nations havent endorsed the target nation')
async def nne_command(interaction, nation_name: str, region_name: str):
    await nations_not_endorsing(interaction, nation_name, region_name)
    
client.run(TOKEN)
