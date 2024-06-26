import json
import random
import requests

headers = {'User-Agent':'KoboBot/1.0'} #request header
#get gems balance
def GetBal(uuid):
    try:
        with open("./dbs/users.json","r") as fi:
            data = json.load(fi)
            gems = data[uuid]["Gems"]#open json to get gems
            fi.close()
            return gems
    except:
        raise ValueError('User Not Set Up')

#set gems
def setGems(uuid: str, amount: int):
    with open("./dbs/users.json", 'r') as fi:
        data = json.load(fi)
    if uuid in data:
        data[uuid]['Gems'] = amount
    with open("./dbs/users.json", 'w') as fi:
        json.dump(data, fi, indent=2)

#query e6
def queryE6(query:str):
    url = 'https://e621.net/posts.json?limit=320&tags='+query
    response = requests.get(url,headers=headers)
    e6data = json.loads(response.content)
    link = e6data['posts'][random.randrange(0,len(e6data['posts']))]['file']['url']
    return str(link)