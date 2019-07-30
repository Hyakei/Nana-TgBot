import os, requests

from bs4 import BeautifulSoup

from nana import app, Owner, Command
from pyrogram import Filters

NamaModul = "Admin List"
HelpCMD = ['`admin <*grup tag/id>` - Melihat semua admin pada grup target']


@app.on_message(Filters.user("self") & Filters.command(["admin", "adminlist"], Command))
def adminlist(client, message):
	try:
		chat = message.text.split(None, 1)[1]
		grup = client.get_chat(chat)
	except:
		chat = message.chat.id
		grup = client.get_chat(chat)
	kek = client.iter_chat_members(chat, filter="administrators")
	creator = []
	admin = []
	badmin = []
	count = 0
	for a in kek:
		count += 1
		try:
			nama = a.user.first_name + " " + a.user.last_name
		except:
			nama = a.user.first_name
		if nama == None:
			nama = "☠️ Akun terhapus"
		if a.status == "administrator":
			if a.user.is_bot == True:
				badmin.append("[{}](tg://user?id={})".format(nama, a.user.id))
			else:
				admin.append("[{}](tg://user?id={})".format(nama, a.user.id))
		elif a.status == "creator":
			creator.append("[{}](tg://user?id={})".format(nama, a.user.id))
	teks = "**Memanggil {} Admin di grup {}**\n".format(len(creator)+len(admin)+len(badmin), grup.title)
	count2 = 0
	teks += "╒═══「 Creator 」\n"
	for x in creator:
		count2 += 1
		teks += "│ • {}\n".format(x)
		if count2 >= 100:
			if message.reply_to_message:
				client.send_message(message.chat.id, teks, reply_to_message_id=message.reply_to_message.message_id, parse_mode="markdown", disable_web_page_preview=True)
			else:
				client.send_message(message.chat.id, teks, parse_mode="markdown", disable_web_page_preview=True)
			teks = ""
			count2 = 0
	teks += "╞══「 {} Human Administrator 」\n".format(len(admin))
	for x in admin:
		count2 += 1
		teks += "│ • {}\n".format(x)
		if count2 >= 100:
			if message.reply_to_message:
				client.send_message(message.chat.id, teks, reply_to_message_id=message.reply_to_message.message_id, parse_mode="markdown", disable_web_page_preview=True)
			else:
				client.send_message(message.chat.id, teks, parse_mode="markdown", disable_web_page_preview=True)
			teks = ""
			count2 = 0
	teks += "╞══「 {} Bot Administrator 」\n".format(len(badmin))
	for x in badmin:
		count2 += 1
		teks += "│ • {}\n".format(x)
		if count2 >= 100:
			if message.reply_to_message:
				client.send_message(message.chat.id, teks, reply_to_message_id=message.reply_to_message.message_id, parse_mode="markdown", disable_web_page_preview=True)
			else:
				client.send_message(message.chat.id, teks, parse_mode="markdown", disable_web_page_preview=True)
			teks = ""
			count2 = 0
	teks += "╘══「 Total {} Admin 」".format(count)
	if count2 >= 1:
		if message.reply_to_message:
			client.send_message(message.chat.id, teks, reply_to_message_id=message.reply_to_message.message_id, parse_mode="markdown", disable_web_page_preview=True)
		else:
			client.send_message(message.chat.id, teks, parse_mode="markdown", disable_web_page_preview=True)
		teks = ""

@app.on_message(Filters.user("self") & Filters.command(["reportadmin"], Command))
def report_admin(client, message):
	message.delete()
	try:
		chat = message.text.split(None, 1)[1]
	except:
		chat = message.chat.id
	grup = client.get_chat(chat)
	kek = client.iter_chat_members(chat, filter="administrators")
	admin = []
	for a in kek:
		if a.status == "administrator" or a.status == "creator":
			if a.user.is_bot == False:
				admin.append('<a href="tg://user?id={}">\u200b</a>'.format(a.user.id))
	if message.reply_to_message:
		teks = '<a href="tg://user?id={}">{}</a> di laporkan ke admin.'.format(message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name)
	else:
		teks = "Memanggil admin di grup {}.".format(grup.title)
	teks += "".join(admin)
	if message.reply_to_message:
		client.send_message(message.chat.id, teks, reply_to_message_id=message.reply_to_message.message_id, parse_mode="html")
	else:
		client.send_message(message.chat.id, teks, parse_mode="html")

@app.on_message(Filters.user("self") & Filters.command(["everyone"], Command))
def AllUsers(client, message):
	message.delete()
	try:
		text = message.text.split(None, 1)[1]
	except:
		text = "Hai semuanya 🙃"
	kek = client.iter_chat_members(message.chat.id)
	everyone = ""
	for a in kek:
		if a.user.is_bot == False:
			everyone += '<a href="tg://user?id={}">\u200b</a>'.format(a.user.id)
	teks = text
	teks += everyone
	if message.reply_to_message:
		client.send_message(message.chat.id, teks, reply_to_message_id=message.reply_to_message.message_id, parse_mode="html")
	else:
		client.send_message(message.chat.id, teks, parse_mode="html")


@app.on_message(Filters.user("self") & Filters.command(["botlist"], Command))
def BotList(client, message):
	try:
		chat = message.text.split(None, 1)[1]
		grup = client.get_chat(chat)
	except:
		chat = message.chat.id
		grup = client.get_chat(chat)
	kek = client.iter_chat_members(chat)
	bots = []
	count = 0
	for a in kek:
		count += 1
		try:
			nama = a.user.first_name + " " + a.user.last_name
		except:
			nama = a.user.first_name
		if nama == None:
			nama = "☠️ Akun terhapus"
		if a.user.is_bot == True:
			bots.append("[{}](tg://user?id={})".format(nama, a.user.id))
	teks = "**Semua bot di grup {}**\n".format(grup.title)
	teks += "╒═══「 Bots 」\n"
	for x in bots:
		teks += "│ • {}\n".format(x)
	teks += "╘══「 Total {} Bots 」".format(len(bots))
	client.send_message(message.chat.id, teks, reply_to_message_id=message.message_id, parse_mode="markdown", disable_web_page_preview=True)

@app.on_message(Filters.user("self") & Filters.command(["admins"], Command))
def CallAdmins(client, message):
	message.delete()
	try:
		chat = message.text.split(None, 2)[1]
		teks = message.text.split(None, 2)[2]
		grup = client.get_chat(chat)
	except:
		chat = message.chat.id
		try:
			teks = message.text.split(None, 1)[1]
		except:
			teks = "Memanggil semua admin di grup {}.".format(grup.title)
		grup = client.get_chat(chat)
	kek = client.iter_chat_members(chat, filter="administrators")
	admin = []
	for a in kek:
		if a.status == "administrator" or a.status == "creator":
			if a.user.is_bot == False:
				admin.append('<a href="tg://user?id={}">\u200b</a>'.format(a.user.id))
	teks += "".join(admin)
	print(teks)
	if message.reply_to_message:
		client.send_message(message.chat.id, teks, reply_to_message_id=message.reply_to_message.message_id, parse_mode="html")
	else:
		client.send_message(message.chat.id, teks, parse_mode="html")
