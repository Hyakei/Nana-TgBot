import time

from nana import app, setbot, AdminSettings
from nana.assistant.database.stickers_db import set_sticker_set, get_sticker_set

from pyrogram import Filters, MessageHandler, InlineKeyboardMarkup, ReplyKeyboardMarkup


TEMP_KEYBOARD = []
USER_SET = {}
TODEL = {}

@setbot.on_message(Filters.user(AdminSettings) & Filters.command(["setsticker"]))
async def get_stickers(client, message):
	global TEMP_KEYBOARD, USER_SET
	await app.send_message("@Stickers", "/stats")
	# app.read_history("@Stickers")
	time.sleep(0.2)
	keyboard = await app.get_history("@Stickers", limit=1)
	keyboard = keyboard[0].reply_markup.keyboard
	for x in keyboard:
		for y in x:
			TEMP_KEYBOARD.append(y)
	await app.send_message("@Stickers", "/cancel")
	msg = await message.reply("Select your stickers for set as kang sticker", reply_markup=ReplyKeyboardMarkup(keyboard))
	USER_SET[message.from_user.id] = msg.message_id
	# app.read_history("@Stickers")

def get_stickerlist(message):
	global TEMP_KEYBOARD, USER_SET
	if message.from_user and message.from_user.id in list(USER_SET):
		return True
	else:
		TEMP_KEYBOARD = []
		USER_SET = {}

@setbot.on_message(get_stickerlist)
async def set_stickers(client, message):
	global TEMP_KEYBOARD, USER_SET
	if message.text in TEMP_KEYBOARD:
		await client.delete_messages(message.chat.id, USER_SET[message.from_user.id])
		set_sticker_set(message.from_user.id, message.text)
		await message.reply("Ok, sticker was set to `{}`".format(message.text))
		TEMP_KEYBOARD = []
		USER_SET = {}
	else:
		await message.reply("Invalid pack selected.")
		TEMP_KEYBOARD = []
		USER_SET = {}
