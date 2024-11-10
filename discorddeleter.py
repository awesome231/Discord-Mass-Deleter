import requests
import time

token = '' # REQUIRED, DO NO SHARE, ENTER YOUR DISCORD TOKEN HERE

guild_id = '' # ENTER SERVER ID HERE ONLY IF YOU WANT TO DELETE FROM A SERVER

user_id = '' # REQUIRED, ENTER YOUR USER ID 

nonserverchannel_id = '' # ENTER THE CHANNEL ID IF YOU WANT IT A DM

isserver = 1 # IMPORTANT!! SET THIS TO 0 FOR DMS AND 1 FOR SERVERS


headers = {
    'authorization': token
}

firstrequest = 0
firstmessage = 0

deletes = 0

offset = 0

length = 0

mid = {}
uid = {}
cid = {}

while True:
    if isserver == 0:
        data = requests.get(f"https://discord.com/api/v9/channels/{nonserverchannel_id}/messages/search?author_id={user_id}", headers=headers)
    elif isserver == 1:        
        data = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/messages/search?author_id={user_id}&offset={offset}", headers=headers)
    data = data.json()
    msgs = data.get("messages", {})
    messageamount = len(msgs)

    a = messageamount
    b = 0

    currentmessage = 0
    if firstrequest == 0:
        while a > b:
            firstmessage = 0
            b += 1
            if currentmessage < messageamount:
                uid[currentmessage] = msgs[currentmessage][0].get('author', {}).get('id')
                mid[currentmessage] = msgs[currentmessage][0].get('id')
                cid[currentmessage] = msgs[currentmessage][0].get('channel_id')
                if uid[currentmessage] == user_id:
                        delete = requests.delete(f'https://discord.com/api/v9/channels/{cid[currentmessage]}/messages/{mid[currentmessage]}', headers=headers)
                        if delete.status_code == 400:
                            offset += 1
                            print(f"FOUND, MID = {mid[currentmessage]} archived, offsetting {offset}")
                        elif delete.status_code == 204:
                            print(f"FOUND, {mid[currentmessage]} successfully deleted")
                        elif delete.status_code == 429:
                            print("you are being rate limited")
                            offset -= 1
                            currentmessage -= 1
                            time.sleep(5)
                        else:
                            input("error")
                            quit()
                        time.sleep(1)
                        currentmessage += 1
                        deletes += 1
                else:
                     print("not one of yours")
                     currentmessage += 1
        if firstmessage == 0:
            msg = {}
            time.sleep(3)
            firstmessage = 1
        else:
            print(f"done!\ndeleted {deletes} messages!")
            input("press enter to stop script")
            quit()
