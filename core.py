from telethon import TelegramClient, sync
from telethon import utils
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.errors.rpcerrorlist import *
from telethon.tl.types import InputPeerChat 
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
		self.current = 0
		self.errores = 0


	async def groupLookout(self,group, client):
		add = []
		try:
			users = await client.get_participants(group)
		except:
			print(group, " whitout users")
			return
		for u in users:
			try:
				username = u.username
			except:
				username = ""
			t = (str(u.id), username, u.first_name, u.last_name, u.phone, 0, )		
			add.append(t)	
		self.database.insertGroup(add)

	async def explore_channels_and_groups(self):
		groups = self.database.listGroups()
		div = len(groups)/ len(self.clients)
		print(self.clients)
		print("Scanning channels and groups")
		counter  = 0
		dif = 0
		for c in self.clients:
			groups_part = groups[counter: counter+int(div)]
			for g in groups_part:
				await self.groupLookout(g[0],c)
				num = int(self.database.stats(0)[0])
				dif = num - dif
				me = await c.get_me()
				print("Scanned group/channel > ", g[0]," by client ",me.phone, "+" +str(dif),"users", num)
				dif = num
		total_users = self.database.stats(0)
		print("users added: ", total_users)


	async def add_to_group(self,group,user):
		self.current+=1
		self.current%= len(self.clients)
		client  = self.clients[self.current]
		id_user = int(user[0][0])
		print("Adding -> ", user ," to", group , " by ", client)
		print("id_user" ,id_user)
		try:
			print(await client.get_entity(id_user))
			await client(InviteToChannelRequest(group,[id_user]))
			self.database.changeStatus((id_user,))
		except(UserPrivacyRestrictedError):
			self.errores+=1
			print(user,  ":-User settings not allow this operation")
			self.database.changeStatusError((id_user,))
		except(UserNotMutualContactError):
			self.errores+=1
			print(user,  ":-The provided user is not a mutual contact")
			self.database.changeStatusError((id_user,))
		except(UserBotError):
			self.errores+=1
			print(user,  ":-The provided user is a bot")
			self.database.changeStatusError((id_user,))
		
	async def add_all_to_group(self,group):
		step = 20.0/len(self.clients)
		user = self.database.selectSome(1)
		while(len(user) > 0):
			
			await self.add_to_group(group,user)
			user = self.database.selectSome(1)
			print("errores", self.errores," ")
			await asyncio.sleep(step)

	async def addToGroup(self,group, arr,client):
		errores = 0
		for user in arr:
			id_user = int(user[0])
			await asyncio.sleep(20)
			print("Adding -> ", user )
			try:	
				await client(InviteToChannelRequest(group,[id_user]))
				self.database.changeStatus((id_user,))
			except(UserPrivacyRestrictedError):
				errores+=1
				print(user,  ":-User settings not allow this operation")
				self.database.changeStatusError((id_user,))
			except(UserNotMutualContactError):
				errores+=1
				print(user,  ":-The provided user is not a mutual contact")
				self.database.changeStatusError((id_user,))
			except(UserBotError):
				errores+=1
				print(user,  ":-The provided user is a bot")
				self.database.changeStatusError((id_user,))
		print('Clients with errors ',errores)

class TelegramaManager:
	def __init__(self,fileUsers, fileChanels,t_group):
		self.fileUsers = fileUsers
		self.fileChanels = fileChanels
		self.database = Database('telegrama4.db')
		self.database.createTable()
		self.telegrama  =  Telegrama(self.database)
		self.target_group = t_group

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
			l = 0
			for row in list_reader:
				g = re.findall(r'([0-9]+)', row[0])
				f = re.findall(r'([0-9a-z]+)', row[1])
				if(len(f[0]) == 32):
					try:
						l+=1
						api_id = int(g[0])
						api_hash = f[0]
						print(api_id, "--")
						client = TelegramClient('client_'+ g[0], api_id, api_hash).start()
						self.telegrama.clients.append(client)
					except:
						pass
			print("Added",len(self.telegrama.clients),"users")
		

