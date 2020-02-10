from telethon import TelegramClient, sync
from telethon import utils
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.errors.rpcerrorlist import *
import asyncio
import threading
import time
from db import Database
import csv
import re
#api_id = 456674 
#api_hash = 'd1c95ef73781413782cd7fcd9115922e'
#group_to_add = ''

#client = TelegramClient('anon', api_id, api_hash).start()

class Telegrama:
	def __init__(self, database):
		self.clients = []
		self.database = database


	def groupLookout(group):
		add = []
		users = self.client.get_participants(group)
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
				print(user,  ":-User settings not allow this operation")
				db.changeStatusError((id_user,))
			except(UserNotMutualContactError):
				errores+=1
				print(user,  ":-The provided user is not a mutual contact")
				db.changeStatusError((id_user,))
			except(UserBotError):
				errores+=1
				print(user,  ":-The provided user is a bot")
				db.changeStatusError((id_user,))
		print('Clients with errors ',errores)

	def lookAllGroups():
		groups = db.listGroups()
		for gr in groups:
			groupLookout(gr[0])

class TelegramaManager:
	def __init__(self,fileUsers, fileChanels):
		self.fileUsers = fileUsers
		self.fileChanels = fileChanels
		self.database = Database('telegrama3.db')
		self.database.createTable()
		self.telegrama  =  Telegrama(self.database)

	def generate_channels(self):
		with open(self.fileChanels, newline='') as csvfile:
			list_reader = csv.reader(csvfile)
			channels = []
			l = 0
			for row in list_reader:
				if(re.match(r'(https://)?t.me/[a-zA-Z0-9_\.]+',row[0])):
					g = re.findall(r'(https://)?t.me/([a-zA-Z0-9_\.]+)', row[0])
					channel = g[0][1]
					l+=1
					channels.append(channel)
			print("Readed groups/channels:",l)
			self.database.addGroups(channels)
			cantidad = self.database.stats(3)
			print("added", cantidad[0], "valid channels/groups.")
		self.database.close()
	def generate_users(self):
		with open(self.fileUsers, newline='') as csvfile:
			list_reader = csv.reader(csvfile)
			users = []
			l = 0
			for row in list_reader:
				g = re.findall(r'([0-9]+)', row[0])
				f = re.findall(r'([0-9a-z]+)', row[1])
				if(len(f[0]) == 32):
					try:
						users.append((int(g[0]),f[0]))
					except:
						pass
			self.telegrama.clients = users
			print("Added",len(users),"users")
		



class TelegramaInput:
	pass