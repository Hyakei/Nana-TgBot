import time
import math
import os
from PIL import Image

from nana import app, setbot, Command
from nana.settings.database.stickers_db import get_sticker_set

from pyrogram import Filters


@app.on_message(Filters.user("self") & Filters.command(["kang"], Command))
def kang_stickers(client, message):
	sticker_pack = get_sticker_set(message.from_user.id)
	if not sticker_pack:
		message.edit("You're not setup sticker pack!\nCheck your assistant for more information!")
		setbot.send_message(message.from_user.id, "Hello 🙂\nYou're look like want to steal a sticker, but sticker pack was not set. To set a sticker pack, type /setsticker and follow setup.")
		return
	sticker_pack = sticker_pack.sticker
	if message.reply_to_message and message.reply_to_message.sticker:
		client.download_media(message.reply_to_message.sticker.file_id, file_name="nana/cache/sticker.png")
	elif message.reply_to_message and message.reply_to_message.photo:
		client.download_media(message.reply_to_message.photo.file_id, file_name="nana/cache/sticker.png")
	else:
		message.edit("Reply a sticker or photo to kang it!\nCurrent sticker pack is: {}".format(sticker_pack))
		return
	im = Image.open("nana/cache/sticker.png")
	maxsize = (512, 512)
	if (im.width and im.height) < 512:
		size1 = im.width
		size2 = im.height
		if im.width > im.height:
			scale = 512 / size1
			size1new = 512
			size2new = size2 * scale
		else:
			scale = 512 / size2
			size1new = size1 * scale
			size2new = 512
		size1new = math.floor(size1new)
		size2new = math.floor(size2new)
		sizenew = (size1new, size2new)
		im = im.resize(sizenew)
	else:
		im.thumbnail(maxsize)
	im.save("nana/cache/sticker.png", 'PNG')
		
	client.send_message("@Stickers", "/addsticker")
	client.read_history("@Stickers")
	time.sleep(0.2)
	client.send_message("@Stickers", sticker_pack)
	client.read_history("@Stickers")
	time.sleep(0.2)
	checkfull = app.get_history("@Stickers", limit=1)[0].text
	if checkfull == "Whoa! That's probably enough stickers for one pack, give it a break. A pack can't have more than 120 stickers at the moment.":
		message.edit("Your sticker pack was full!\nPlease change one from your Assistant")
		return
	client.send_document("@Stickers", 'nana/cache/sticker.png')
	os.remove('nana/cache/sticker.png')
	try:
		ic = message.text.split(None, 1)[1]
	except:
		try:
			ic = message.reply_to_message.sticker.emoji
		except:
			ic = "🤔"
	if ic == None:
		ic = "🤔"
	client.send_message("@Stickers", ic)
	client.read_history("@Stickers")
	time.sleep(1)
	client.send_message("@Stickers", "/done")
	message.edit("**Sticker added!**\nYour sticker has been saved on [This sticker pack](https://t.me/addstickers/{})".format(sticker_pack))
	client.read_history("@Stickers")
