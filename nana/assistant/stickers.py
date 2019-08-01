import time

from nana import app, setbot, AdminSettings
from nana.assistant.database.stickers_db import set_sticker_set, get_sticker_set

from pyrogram import Filters, MessageHandler, InlineKeyboardMarkup, ReplyKeyboardMarkup


TEMP_KEYBOARD = []
USER_SET = {}
TODEL = {}

@setbot.on_message(Filters.user(AdminSettings) & Filters.command(["setsticker"]))
def get_stickers(client, message):
	global TEMP_KEYBOARD, USER_SET
	app.send_message("@Stickers", "/stats")
	app.read_history("@Stickers")
	time.sleep(0.2)
	keyboard = app.get_history("@Stickers", limit=1)[0].reply_markup.keyboard
	for x in keyboard:
		for y in x:
			TEMP_KEYBOARD.append(y)
	app.send_message("@Stickers", "/cancel")
	msg = message.reply("Select your stickers for set as kang sticker", reply_markup=ReplyKeyboardMarkup(keyboard))
	USER_SET[message.from_user.id] = msg.message_id
	app.read_history("@Stickers")

def get_stickerlist(message):
	global TEMP_KEYBOARD, USER_SET
	if message.from_user and message.from_user.id in list(USER_SET):
		return True
	else:
		TEMP_KEYBOARD = []
		USER_SET = {}

@setbot.on_message(get_stickerlist)
def set_stickers(client, message):
	global TEMP_KEYBOARD, USER_SET
	if message.text in TEMP_KEYBOARD:
		client.delete_messages(message.chat.id, USER_SET[message.from_user.id])
		set_sticker_set(message.from_user.id, message.text)
		message.reply("Ok, sticker was set to `{}`".format(message.text))
		TEMP_KEYBOARD = []
		USER_SET = {}
	else:
		message.reply("Invalid pack selected.")
		TEMP_KEYBOARD = []
		USER_SET = {}
