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
import internalFunction as iF
from discord import app_commands
import discord.ext.commands
from discord.ext import commands
import requests
import json
import discord.ext
from typing import List
from typing import Optional
from typing import Union
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
guid = discord.Object(id=Constants.guild_id)

@client.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')
        #custom user settings

##############tree commands
@tree.command(name='yip',description='ping the bot',guild=guid) #ping
async def yip(interaction: discord.Interaction):
    await interaction.response.send_message('Yap!')


##############Gambling
@tree.command(name="bal",description="get your gem balance",guild=guid)
async def bal(interaction: discord.Interaction):
    try:
        with open("./dbs/users.json","r") as fi:
            gems = iF.GetBal(str(int(interaction.user.id)))#open json to get gems
            await interaction.response.send_message("Gems: "+str(gems))
        fi.close()
    except:
        await interaction.response.send_message("use /user Setup")

@tree.command(name="flip",description="flip a coin for X amout of gems and earn 1.25X!!",guild=guid)#flip a coin
async def flip(interaction: discord.Interaction,ammount:str|None):
    await interaction.response.defer()
    try:
        bet = float(int(ammount))
    except:
        bet = 0
    try:
        gems = iF.GetBal(str(int(interaction.user.id)))#open json to get gems
    except:
        await interaction.followup.send("use /user Setup")
    try:
        if ammount == None and gems > 0 and bet <= gems:
            bet = 1
            flip = random.randint(0,1)
            await interaction.followup.send("Bet: "+str(bet))
            if flip == 1:
                reward = int(bet*0.5)
                iF.setGems(str(int(interaction.user.id)),iF.GetBal(str(int(interaction.user.id)))+1)
                strReward=str(reward+1)
                await interaction.followup.send("You Earned! "+strReward+ " AGAIN!!!")
            else:
                reward = -(int(bet))
                iF.setGems(str(int(interaction.user.id)),iF.GetBal(str(int(interaction.user.id)))+reward)
                strReward=str(abs(reward))
                await interaction.followup.send(f"You lost! "+strReward+" But try again, All gamblers quit before they win")
        elif gems > 0 and bet <= gems:
            flip = random.randint(0,1)
            await interaction.followup.send("Bet: "+str(bet))
            if flip == 1:
                reward = int(bet*0.5)
                iF.setGems(str(int(interaction.user.id)),iF.GetBal(str(int(interaction.user.id)))+reward)
                strReward=str(reward)
                await interaction.followup.send("You Earned! "+strReward+ " AGAIN!!!")
            else:
                reward = -(int(bet))
                iF.setGems(str(int(interaction.user.id)),iF.GetBal(str(int(interaction.user.id)))+reward)
                strReward=str(abs(reward))
                await interaction.followup.send(f"You lost! "+strReward+" But try again, All gamblers quit before they win")
    except:
        await interaction.followup.send('Enter A Valid Number')

#######################
@tree.command(name='user',description='user setup and information',guild=guid)#user setup
async def user(interaction: discord.Interaction, command:str, input: str | None):
    if command == 'Setup' or command == 'setup':
        with open("./dbs/users.json", 'r') as fi:
            data = json.load(fi)
            if str(int(interaction.user.id)) in data: #if existing reset gems
                if input == None:
                    data[str(int(interaction.user.id))] = {"name":str(interaction.user.name),"pronouns":data[str(int(interaction.user.id))]["pronouns"],"Gems": 500}
                else:
                    data[str(int(interaction.user.id))] = {"name":str(interaction.user.name),"pronouns":input,"Gems": 500}
            else:
                if input == None:
                    data[str(int(interaction.user.id))] = {"name":str(interaction.user.name),"pronouns":"","Gems": 500}
                else:
                    data[str(int(interaction.user.id))] = {"name":str(interaction.user.name),"pronouns":input,"Gems": 500}
            print("name:",str(interaction.user.name),"pron:",input)
        fi.close()
        with open("./dbs/users.json", 'w') as fi:
            json.dump(data, fi, indent=2)
        fi.close()
        await interaction.response.send_message('setup Complete')
@user.autocomplete('command')
async def input_auto(
    interaction:discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    commands = ['setup']
    return [
        app_commands.Choice(name=input, value=input)
        for input in commands if current.lower() in input.lower()
    ]
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
        jsonData = json.load(fi)
        prons=jsonData[str(int(interaction.user.id))]["pronouns"]
    await interaction.response.defer()
    await interaction.followup.send('`due to low processing power this may take some time`')
    await client.change_presence(status=discord.Status.online,activity=discord.CustomActivity('⚙️...Processing...⚙️'))
    try:
        jsonreq = {
        "model":"llama3",
        "stream":True,
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
        await interaction.followup.send(str(resp["response"]))
        fi.close()
    except:
        jsonreq = {
        "model":"llama3",
        "stream":True,
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
        print(str(resp))
        await interaction.followup.send(str(resp["response"]))
        fi.close()
    await client.change_presence(status=discord.Status.online,activity=discord.CustomActivity('Watching You and Vibin'))
#####################
######IMAGES######
@tree.command(name='e6',description='Query the funny website at your own risk (Split queries by a plus sign no spaces)',nsfw=True,guild=guid)
async def e6(interaction: discord.Interaction,query: str | None):
    await interaction.response.send_message('|| '+iF.queryE6(query)+' ||')
@tree.command(name='safe6',description='Query the funny website at your own risk (Split queries by a plus sign no spaces) now with a safty',nsfw=False,guild=guid)
async def Safe6(interaction: discord.Interaction,query: str | None):
    await interaction.response.send_message(iF.queryE6(query+'+rating:s'))

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