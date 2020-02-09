from telethon import TelegramClient
from telethon import utils

# me = await client.get_entity('me')
# print(utils.get_display_name(me))

# chat = await client.get_input_entity('username')

api_id = 456674 
api_hash = 'd1c95ef73781413782cd7fcd9115922e'


with TelegramClient('anon', api_id, api_hash) as client:
	# print(client)
	for message in client.iter_messages('me'):
		print(message)
