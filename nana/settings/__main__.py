import os, requests

from bs4 import BeautifulSoup

from nana import app, setbot, Owner, DB_AVAIABLE
from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton



@setbot.on_message(Filters.user(Owner) & Filters.command(["start"]))
def start(client, message):
	me = app.get_me()
	text = "Hello {}!\n".format(message.from_user.first_name)
	text += "**Here is your current stats:**\n"
	text += "-> Userbot: `Running (v0.1)`\n"
	text += "Logged in as `{}`\n".format(me.first_name)
	text += "-> Bot Settings: `Running (v0.1)`\n"
	text += "-> Database: `{}`".format(DB_AVAIABLE)
	message.reply(text)

@setbot.on_message(Filters.user(Owner) & Filters.command(["getme"]))
def get_myself(client, message):
	me = app.get_me()
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
	button = InlineKeyboardMarkup([[InlineKeyboardButton("Hide phone number", callback_data="hide_number")]])
	if me.photo:
		client.send_photo(message.chat.id, photo=getpp, caption=text, reply_markup=button)
	else:
		message.reply(text, reply_markup=button)


# For callback query button
def dynamic_data_filter(data):
	return Filters.create(
		lambda flt, query: flt.data == query.data,
		data=data  # "data" kwarg is accessed with "flt.data" above
	)

@setbot.on_callback_query(dynamic_data_filter("hide_number"))
def get_myself_btn(client, query):
	me = app.get_me()
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

	if query.message.caption:
		query.message.edit_caption(caption=text, reply_markup=button)
	else:
		query.message.edit(text, reply_markup=button)
