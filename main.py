import discord
from discord import app_commands
from credentials import TOKEN
from functions.dispatch_c import dispatch
from functions.WA.ga_c import ga
from functions.nation_c import nation
from functions.nne_c import nations_not_endorsing
from functions.privateshards.nationregistration import nation_register
from functions.privateshards.dispatch_writer import dispatch_write


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

@tree.command(name = 'register', description='Register a nation to access its private shards')
async def register_command(interaction, nation_name: str, nation_password: str):
    await nation_register(interaction, nation_name, nation_password)

@tree.command(name = 'dispatchwrite', description='To write a dispatch using a registered nation')
async def write_command(interaction, title: str, body: str):
    await dispatch_write(interaction, title, body)

@tree.command(name = 'sc', description='To see information about a Security Council proposal')
async def sc_command(interaction, proposal_id: int):
    await sc(interaction, proposal_id)

client.run(TOKEN)
