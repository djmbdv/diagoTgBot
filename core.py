from telethon import TelegramClient, sync
from telethon import utils
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.errors.rpcerrorlist import *
import asyncio
import threading
import time
import db

api_id = 456674 
api_hash = 'd1c95ef73781413782cd7fcd9115922e'
group_to_add = ''

client = TelegramClient('anon', api_id, api_hash).start()

def groupLookout(group):
	add = []
	users = client.get_participants(group)
	for u in users:
		t = (str(u.id), u.username, u.first_name, u.last_name, u.phone, 0, )		
		add.append(t)	
	db.insertGroup(add)

async def addToGroup(group, arr):
	errores = 0
	for user in arr:
		id_user = int(user[0])
		await asyncio.sleep(5)
		print("Agregando a ", user )
		try:
			print()		
			await client(InviteToChannelRequest(group,[id_user]))
			db.changeStatus((id_user,))
		except(UserPrivacyRestrictedError):
			errores+=1
			print(user,  ": Usuario no permite por su configuracion")
			db.changeStatusError((id_user,))
		except(UserNotMutualContactError):
			errores+=1
			print(user,  ":The provided user is not a mutual contact")
			db.changeStatusError((id_user,))
		except(UserBotError):
			errores+=1
			print(user,  ":The provided user is a bot")
			db.changeStatusError((id_user,))
	print('Usuarios con errores> ',errores)

def lookAllGroups():
	groups = db.listGroups()
	for gr in groups:
		groupLookout(gr[0])

