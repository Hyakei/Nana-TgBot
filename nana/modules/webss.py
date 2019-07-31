import os, shutil, requests

from nana import app, Command, thumbnail_API, screenshotlayer_API
from pyrogram import Filters

NamaModul = "Screenshot Website"
HelpCMD = ['`print <url>` - Menscreenshot depan website',
'`ss <url>` - Menscreenshot full website']

bantuan = """
**Penggunaan print web:**
`/print <website>`
Contoh: `/print google.com`
"""

@app.on_message(Filters.user("self") & Filters.command(["print"], Command))
def ssweb(client, message):
	if len(message.text.split()) == 1:
		message.edit(bantuan)
		return
	if not thumbnail_API:
		message.edit("You need to fill thumbnail_API to use this!")
		return
	message.edit("Please wait...")
	args = message.text.split(None, 1)
	teks = args[1]
	if "http://" in teks or "https://" in teks:
		teks = teks
	else:
		teks = "http://" + teks
	capt = "Website: `{}`".format(teks)

	client.send_chat_action(message.chat.id, action="upload_photo")
	r = requests.get("https://api.thumbnail.ws/api/{}/thumbnail/get?url={}&width=1280".format(thumbnail_API, teks), stream=True)
	if r.status_code != 200:
		message.edit(r.text, disable_web_page_preview=True)
		return
	with open("nana/cache/web.png", "wb") as stk:
		shutil.copyfileobj(r.raw, stk)
	client.send_photo(message.chat.id, photo="nana/cache/web.png", caption=capt, reply_to_message_id=message.message_id)
	os.remove("nana/cache/web.png")
	client.send_chat_action(message.chat.id, action="cancel")
	message.edit(capt)

@app.on_message(Filters.user("self") & Filters.command(["ss"], Command))
def ssweb(client, message):
	if len(message.text.split()) == 1:
		message.edit(bantuan)
		return
	if not screenshotlayer_API:
		message.edit("You need to fill screenshotlayer_API to use this!")
		return
	message.edit("Please wait...")
	args = message.text.split(None, 1)
	teks = args[1]
	full = False
	if len(message.text.split()) >= 3:
		if message.text.split(None, 2)[2] == "full":
			full = True

	if "http://" in teks or "https://" in teks:
		teks = teks
	else:
		teks = "http://" + teks
	capt = "Website: `{}`".format(teks)

	client.send_chat_action(message.chat.id, action="upload_photo")
	if full:
		r = requests.get("http://api.screenshotlayer.com/api/capture?access_key={}&url={}&fullpage=1".format(screenshotlayer_API, teks), stream=True)
	else:
		r = requests.get("http://api.screenshotlayer.com/api/capture?access_key={}&url={}&fullpage=0".format(screenshotlayer_API, teks), stream=True)

	try:
		catcherror = r.json()
		if not catcherror['success']:
			message.edit(r.json(), disable_web_page_preview=True)
			return
	except:
		pass
	
	with open("nana/cache/web.png", "wb") as stk:
		for chunk in r:
			stk.write(chunk)

	client.send_document(message.chat.id, document="nana/cache/web.png", caption=capt, reply_to_message_id=message.message_id)
	os.remove("nana/cache/web.png")
	client.send_chat_action(message.chat.id, action="cancel")
	message.edit(capt)
