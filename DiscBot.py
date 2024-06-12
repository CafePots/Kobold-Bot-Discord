#########################################
#					                    #
#	< Discord Bot By Cafe >		        #
#					                    #
#	probably not any good lol,	        #
#	just doing some experimenting	    #
#	with the API and such		        #
#					                    #
#					                    #
######################################### 

print("Loading...")
import discord
import Constants
from discord import app_commands
import discord.ext.commands
from discord.ext import commands
import requests
import json
import discord.ext
from typing import List
from typing import Optional
from typing import Union

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
guid = discord.Object(id=1247589243895939295)

@client.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')
        #custom user settings

##############tree commands
@tree.command(name='yip',description='ping the bot',guild=guid) #ping
async def yip(interaction: discord.Interaction):
    await interaction.response.send_message('Yap!')



#######################
@tree.command(name='user',description='user setup and information',guild=guid)
async def user(interaction: discord.Interaction, command:str, input: str | None):
    if command == 'Setup' or command == 'setup':
        with open("./dbs/users.json","w") as fi:
            y = {
                    str(int(interaction.user.id)):{
                    "name":str(interaction.user.name),
                    "pronouns":input
                    }
                }
            json.dump(json.dumps(y),fi) 
            print("name:",str(interaction.user.name),"pron:",input)
        fi.close()
        await interaction.response.send_message('setup Complete')
@user.autocomplete('input')
async def input_auto(
    interaction:discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    pronouns = ['he/Him', 'he/they', 'they/them', 'she/they', 'she/her']
    return [
        app_commands.Choice(name=input, value=input)
        for input in pronouns if current.lower() in input.lower()
    ]
##################
@tree.command(name='cafe',description='ask cafe a question!',guild=guid) #ai command
async def cafe(interaction: discord.Interaction, question: str|None):
    url = 'http://localhost:11434/api/generate'
    with open("./dbs/users.json","r") as fi:
        jsonData = json.loads(str(json.load(fi)))
        prons=jsonData[str(int(interaction.user.id))]["pronouns"]
    await interaction.response.send_message('`due to low processing power this may take some time`')
    await client.change_presence(status=discord.Status.online,activity=discord.CustomActivity('⚙️...Processing...⚙️'))
    try:
        jsonreq = {
        "model":"llama3",
        "stream":False,
        "prompt":f"your name is Cafe-Bot a small kobold assistant that wants to help as much as possible. Always \
                     start and end your responce with 'Yip!' while keeping your responces as short as possible, \
                     also here is a set of rules to follow if you want to format your fonts, \
                     use * around words to use italics, You can use ** around words to bold them, you can use *** around words to make it bold and italic, \
                     use __ aroud words to underline them, use #, ##, and ### before a line to make them a big header, medium header, and small header sized respectively. \
                     you can create lists with - before a line, for a small code block use ` around the code and for a large code block use ``` around the code. \
                     for a block quote you can add > before a line \
                     this user's name is {str(interaction.user.name)} and pronouns are {str(prons)} and respond only to the following message: "+str(question)
        }
        resp = requests.post(url,json=jsonreq)
        resp = json.loads(str(resp.text))
        print(str(resp["response"]))
        await interaction.response.send_message(str(resp["response"]))
        fi.close()
    except:
        jsonreq = {
        "model":"llama3",
        "stream":False,
        "prompt":f"your name is Cafe-Bot a small kobold assistant that wants to help as much as possible. Always \
                     start and end your responce with 'Yip!' while keeping your responces as short as possible, \
                     also here is a set of rules to follow if you want to format your fonts, \
                     use * around words to use italics, You can use ** around words to bold them, you can use *** around words to make it bold and italic, \
                     use __ aroud words to underline them, use #, ##, and ### before a line to make them a big header, medium header, and small header sized respectively. \
                     you can create lists with - before a line, for a small code block use ` around the code and for a large code block use ``` around the code. \
                     for a block quote you can add > before a line \
                     this user's name is {str(interaction.user.name)} respond only to the following message: "+str(question)
        }
        resp = requests.post(url,json=jsonreq)
        resp = json.loads(str(resp.text))
        print(str(resp["response"]))
        await interaction.response.send_message(str(resp["response"]))
        fi.close()
    await client.change_presence(status=discord.Status.online,activity=discord.CustomActivity('Watching You and Vibin'))
#####################
########Moderation##########


@tree.command(name='kill',description='ban one or many',guild=guid)
@discord.app_commands.checks.has_permissions(ban_members=True)
async def kill(interaction: discord.Interaction, user: Union[discord.Member,discord.Member], delete_days: int|None,reason: str|None):
    discord.Guild.ban(user,delete_message_days=delete_days,reason=reason)
    await interaction.response.send_message(f'Banned {user}')


########"Moderation"##########
def is_me():
    def predicate(interaction: discord.Interaction) -> bool:
        return interaction.user.id == 704411711012078140
    return app_commands.check(predicate)

@tree.command(name='nokill',description='ban one or many',guild=guid)
@is_me()
async def nokill(interaction: discord.Interaction, user:Union[discord.Member,discord.Member], delete_days: int|None,reason: str|None):
    discord.Guild.ban(user,delete_message_days=delete_days,reason=reason)
    await interaction.response.send_message(f'Banned {user}')
###############################

@client.event
async def on_ready():
    await tree.sync(guild=guid)
    await client.change_presence(status=discord.Status.online,activity=discord.CustomActivity('Watching You and Vibin'))
    print(f'Logged on as {client.user}!')

client.run(Constants.API_KEY)