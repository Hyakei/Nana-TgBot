import os
import requests
import shutil

from nana import app, Command
from pyrogram import Filters


__MODULE__ = "Uploader image"
__HELP__ = """
Reupload URL image to telegram without save it first.

──「 **Upload image** 」──
-> `pic`
Upload image from URL

──「 **Upload sticker** 」──
-> `stk`
Upload image and convert to sticker, please note image from telegraph will result bug (telegram bugs)
"""


@app.on_message(Filters.user("self") & Filters.command(["pic"], Command))
def PictureUploader(client, message):
	if len(message.text.split()) == 1:
		message.edit("Usage: `.pic <url>`")
		return
	photo = message.text.split(None, 1)[1]
	message.delete()
	if "http" in photo:
		r = requests.get(photo, stream=True)
		with open("nana/cache/pic.png", "wb") as stk:
			shutil.copyfileobj(r.raw, stk)
		if message.reply_to_message:
			client.send_photo(message.chat.id, "nana/cache/pic.png", reply_to_message_id=message.reply_to_message.message_id)
		else:
			client.send_photo(message.chat.id, "nana/cache/pic.png")
		os.remove("nana/cache/pic.png")
	else:
		if message.reply_to_message:
			client.send_photo(message.chat.id, photo, caption, reply_to_message_id=message.reply_to_message.message_id)
		else:
			client.send_photo(message.chat.id, photo, caption)

@app.on_message(Filters.user("self") & Filters.command(["stk"], Command))
def StickerUploader(client, message):
	if len(message.text.split()) == 1:
		message.edit("Usage: `.stk <url>`")
		return
	photo = message.text.split(None, 1)[1]
	message.delete()
	if "http" in photo:
		r = requests.get(photo, stream=True)
		with open("nana/cache/stiker.png", "wb") as stk:
			shutil.copyfileobj(r.raw, stk)
		if message.reply_to_message:
			client.send_sticker(message.chat.id, "nana/cache/stiker.png", reply_to_message_id=message.reply_to_message.message_id)
		else:
			client.send_sticker(message.chat.id, "nana/cache/stiker.png")
		os.remove("nana/cache/stiker.png")
	else:
		if message.reply_to_message:
			client.send_sticker(message.chat.id, photo, reply_to_message_id=message.reply_to_message.message_id)
		else:
			client.send_sticker(message.chat.id, photo)
