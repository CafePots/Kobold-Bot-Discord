import json

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

