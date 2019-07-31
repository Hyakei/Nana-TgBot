import pyrogram
import os

from gtts import gTTS
from nana import app, Command
from pyrogram import Filters

NamaModul = "Voice TTS"
HelpCMD = ['`voice <*lang> <teks>` - Mengirim TTS auto generated dari google']

bantuan = """Penggunaan:
`/voice <bahasa> <kata>`
Contoh: `/voice en hello`
Output: `voice`
Atau
`/voice <kata>`
Contoh: `/voice hello`
Output: `voice`"""

# TODO setlang

@app.on_message(Filters.user("self") & Filters.command(["voice"], Command))
def voice(client, message):
	if len(message.text.split()) == 1:
		message.edit(bantuan)
		return
	message.delete()
	client.send_chat_action(message.chat.id, "record_audio")
	text = message.text.split(None, 1)[1]
	tts = gTTS(text, lang="en")
	tts.save('nana/cache/voice.mp3')
	if message.reply_to_message:
		client.send_voice(message.chat.id, voice="nana/cache/voice.mp3", reply_to_message_id=message.reply_to_message.message_id)
	else:
		client.send_voice(message.chat.id, voice="nana/cache/voice.mp3")
	client.send_chat_action(message.chat.id, action="cancel")
	os.remove("nana/cache/voice.mp3")
