import os

from nana import app, Command
from pyrogram import Filters
from nana.modules.database.chats_db import update_chat, get_all_chats


@app.on_message(Filters.group, group=10)
def UpdateMyChats(client, message):
	update_chat(message.chat)


@app.on_message(Filters.user("self") & Filters.command(["chatlist"], Command))
def get_chat(client, message):
	all_chats = get_all_chats()
	chatfile = 'List of chats that I joined.\n'
	for chat in all_chats:
		if str(chat.chat_username) != "None":
			chatfile += "{} - ({}): @{}\n".format(chat.chat_name, chat.chat_id, chat.chat_username)
		else:
			chatfile += "{} - ({})\n".format(chat.chat_name, chat.chat_id)

	with open("chatlist.txt", "w") as writing:
		writing.write(str(chatfile))
		writing.close()

	client.send_document("self", document="chatlist.txt", caption="Here is the chat list that I joined.")
	message.edit("My chat list exported to my saved messages.")
	os.remove("chatlist.txt")
