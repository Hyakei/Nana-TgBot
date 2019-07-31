import os, requests

from bs4 import BeautifulSoup

from nana import app, setbot, Owner, AdminSettings, DB_AVAIABLE, USERBOT_VERSION, SETTINGSBOT_VERSION
from __main__ import reload_userbot
from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton, errors

from threading import Thread


@setbot.on_message(Filters.user(AdminSettings) & Filters.command(["start"]))
def start(client, message):
	try:
		me = app.get_me()
	except ConnectionError:
		me = None
	text = "Hello {}!\n".format(message.from_user.first_name)
	text += "**Here is your current stats:**\n"
	if not me:
		text += "-> Userbot: `Stopped (v{})`\n".format(USERBOT_VERSION)
	else:
		text += "-> Userbot: `Running (v{})`\n".format(USERBOT_VERSION)
	text += "-> Bot Settings: `Running (v{})`\n".format(SETTINGSBOT_VERSION)
	text += "-> Database: `{}`\n".format(DB_AVAIABLE)
	if not me:
		text += "\nBot is currently turned off, to start bot again, type /settings and click **Start Bot** button"
	else:
		text += "\nBot logged in as `{}`\nTo get more information about this user, type /getme\n".format(me.first_name)
	message.reply(text)

@setbot.on_message(Filters.user(AdminSettings) & Filters.command(["getme"]))
def get_myself(client, message):
	try:
		me = app.get_me()
	except ConnectionError:
		message.reply("Bot is currently turned off!")
		return
	getphoto = client.get_profile_photos(me.id)
	if len(getphoto) == 0:
		getpp = None
	else:
		getpp = getphoto[0].file_id
	text = "**ℹ️ Your profile:**\n"
	text += "First name: {}\n".format(me.first_name)
	if me.last_name:
		text += "Last name: {}\n".format(me.last_name)
	text += "User ID: `{}`\n".format(me.id)
	if me.username:
		text += "Username: @{}\n".format(me.username)
	text += "Phone number: `{}`\n".format(me.phone_number)
	text += "`Nana Version    : v{}`\n".format(USERBOT_VERSION)
	text += "`Manager Version : v{}`".format(SETTINGSBOT_VERSION)
	button = InlineKeyboardMarkup([[InlineKeyboardButton("Hide phone number", callback_data="hide_number")]])
	if me.photo:
		client.send_photo(message.chat.id, photo=getpp, caption=text, reply_markup=button)
	else:
		message.reply(text, reply_markup=button)


@setbot.on_message(Filters.user(AdminSettings) & Filters.command(["settings"]))
def settings(client, message):
	try:
		me = app.get_me()
	except ConnectionError:
		me = None
	text = "**⚙️ Welcome to Nana Settings!**\n"
	if not me:
		text += "-> Userbot: `Stopped (v{})`\n".format(USERBOT_VERSION)
	else:
		text += "-> Userbot: `Running (v{})`\n".format(USERBOT_VERSION)
	text += "-> Bot Settings: `Running (v{})`\n".format(SETTINGSBOT_VERSION)
	text += "-> Database: `{}`\n".format(DB_AVAIABLE)
	text += "\nJust setup what you need here"
	if not me:
		togglestart = "Start Bot"
	else:
		togglestart = "Stop Bot"
	button = InlineKeyboardMarkup([[InlineKeyboardButton(togglestart, callback_data="toggle_startbot")]])
	message.reply(text, reply_markup=button)


# For callback query button
def dynamic_data_filter(data):
	return Filters.create(
		lambda flt, query: flt.data == query.data,
		data=data  # "data" kwarg is accessed with "flt.data" above
	)

@setbot.on_callback_query(dynamic_data_filter("hide_number"))
def get_myself_btn(client, query):
	try:
		me = app.get_me()
	except ConnectionError:
		client.answer_callback_query(query.id, "Bot is currently turned off!", show_alert=True)
		return
	getphoto = client.get_profile_photos(me.id)
	if len(getphoto) == 0:
		getpp = None
	else:
		getpp = getphoto[0].file_id

	text = "**ℹ️ Your profile:**\n"
	text += "First name: {}\n".format(me.first_name)
	if me.last_name:
		text += "Last name: {}\n".format(me.last_name)
	text += "User ID: `{}`\n".format(me.id)
	if me.username:
		text += "Username: @{}\n".format(me.username)

	currtext = query.message.text or query.message.caption
	if "***" not in currtext.markdown.split("Phone number: `")[1].split("`")[0]:
		num = []
		num.append("*"*len(me.phone_number))
		text += "Phone number: `{}`\n".format("".join(num))
		button = InlineKeyboardMarkup([[InlineKeyboardButton("Show phone number", callback_data="hide_number")]])
	else:
		text += "Phone number: `{}`\n".format(me.phone_number)
		button = InlineKeyboardMarkup([[InlineKeyboardButton("Hide phone number", callback_data="hide_number")]])

	text += "`Nana Version    : v{}`\n".format(USERBOT_VERSION)
	text += "`Manager Version : v{}`".format(SETTINGSBOT_VERSION)

	if query.message.caption:
		query.message.edit_caption(caption=text, reply_markup=button)
	else:
		query.message.edit(text, reply_markup=button)

@setbot.on_callback_query(dynamic_data_filter("toggle_startbot"))
def start_stop_bot(client, query):
	try:
		me = app.get_me()
	except ConnectionError:
		reload_userbot()
		text = "**⚙️ Welcome to Nana Settings!**\n"
		text += "-> Userbot: `Running (v{})`\n".format(USERBOT_VERSION)
		text += "-> Bot Settings: `Running (v{})`\n".format(SETTINGSBOT_VERSION)
		text += "-> Database: `{}`\n".format(DB_AVAIABLE)
		text += "\n✅ Bot was started!"
		button = InlineKeyboardMarkup([[InlineKeyboardButton("Stop Bot", callback_data="toggle_startbot")]])
		try:
			query.message.edit_text(text, reply_markup=button)
		except errors.exceptions.bad_request_400.MessageNotModified:
			pass
		client.answer_callback_query(query.id, "Bot was started!")
		return
	app.stop()
	text = "**⚙️ Welcome to Nana Settings!**\n"
	text += "-> Userbot: `Stopped (v{})`\n".format(USERBOT_VERSION)
	text += "-> Bot Settings: `Running (v{})`\n".format(SETTINGSBOT_VERSION)
	text += "-> Database: `{}`\n".format(DB_AVAIABLE)
	text += "\n❎ Bot was stopped!"
	button = InlineKeyboardMarkup([[InlineKeyboardButton("Start Bot", callback_data="toggle_startbot")]])
	try:
		query.message.edit_text(text, reply_markup=button)
	except errors.exceptions.bad_request_400.MessageNotModified:
		pass
	client.answer_callback_query(query.id, "Bot was stopped!")


@setbot.on_callback_query(dynamic_data_filter("report_errors"))
def report_some_errors(client, query):
	text = "Hi @AyraHikari, i got an error for you.\nPlease take a look and fix it if possible.\n\nThank you ❤️"
	err = query.message.text
	open("nana/cache/errors.txt", "w").write(err)
	query.message.edit_reply_markup(reply_markup=None)
	app.send_document("EmiliaOfficial", "nana/cache/errors.txt", caption=text)
	os.remove("nana/cache/errors.txt")
	client.answer_callback_query(query.id, "Report was sent!")
