from telethon import TelegramClient, sync
from telethon import utils
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
import db

# me = await client.get_entity('me')
# print(utils.get_display_name(me))

# chat = await client.get_input_entity('username')

api_id = 456674 
api_hash = 'd1c95ef73781413782cd7fcd9115922e'

# with TelegramClient('anon', api_id, api_hash) as client:
# class telegram_client:
# 	def __init__(self, id, username, fname, lname, phone, status):
# 		self.id = id
# 		self.username = username
# 		self.fname = fname
# 		self.lname = lname
# 		self.phone = phone
# 		self.status = status


client = TelegramClient('anon', api_id, api_hash).start()
add = []

# participants = client.get_participants('DbFirReRnqxjYpQlwJRQuw')

users = client.get_participants('AudiosdeMarcuxx')
# print(len(users))
# t1 = telegram_client(users[0].id, users[0].username, users[0].first_name, users[0].last_name, users[0].phone, 0)
# t1 = (users[0].id, users[0].username, users[0].first_name, users[0].last_name, users[0].phone, 0)
# print(t1)
# add.append(t1)
# print(add[0].__dict__)
# t2 = (users[1].id, users[1].username, users[1].first_name, users[1].last_name, users[1].phone, 0)
# add.append(t2)
# print(add)
###for u in users:
	# t = (str(u.id), u.username, u.first_name, u.last_name, u.phone, 0, )
	# add.append(t)

# db.insertGroup(add)
# print(add)

# print(users[2].id)
# print(users[2].first_name)
# print(users[2].last_name)
# print(users[2].username)
# print(users[2].phone)


# for u in user:
#     print(u)
# for p in participants:
#     print(p)

full = client(GetFullUserRequest('djmbdv'))

bio = full.about

print(full)

# client(InviteToChannelRequest(
#     'AudiosdeMarcuxx',
#     [292917466]
# ))
