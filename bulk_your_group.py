from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest

api_id = 456674 
api_hash = 'd1c95ef73781413782cd7fcd9115922e'

user = await client.get_input_entity('username')

with TelegramClient('anon', api_id, api_hash) as client:
    client.loop.run_until_complete(client.send_message('me', 'Hello, myself!'))
    
chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue


i=0
for g in groups:
    print(str(i) + '- ' + g.title)
    i+=1


# Show all user IDs in a chat
async for user in client.iter_participants(chat):
    print(user.id)

users = await client.get_participants(chat)
print(users[0].first_name)

for user in users:
    if user.username is not None:
        print(user.username)