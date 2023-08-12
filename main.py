import discord
from discord import app_commands
from credentials import TOKEN
from functions.dispatch_c import dispatch
from functions.WA.ga_c import ga
from functions.WA.sc_c import sc
from functions.nation_c import nation
from functions.region_c import region
from functions.verify_c import verify
from modfunctions.help_c import help

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

@tree.command(name = 'region', description='To see information about a particular region')
async def region_command(interaction, region_name: str):
    await region(interaction, region_name)

@tree.command(name='ga', description='To see information about the General Assembly')
async def ga_command(interaction, proposal_id: int):
    await ga(interaction, proposal_id)

@tree.command(name='dispatch', description='To see information about a dispatch')
async def dispatch_command(interaction, dispatch_link: str):
    await dispatch(interaction, dispatch_link)

@tree.command(name = 'sc', description='To see information about a Security Council proposal')
async def sc_command(interaction, proposal_id: int):
    await sc(interaction, proposal_id)
    
@tree.command(name = 'verify', description="Verifies a user's nation")
async def verify_command(interaction, nation: str):
    await verify(interaction, nation, client)

@tree.command(name = 'help', description='Commands List')
async def help_command(interaction):
    await help(interaction)

client.run(TOKEN)

