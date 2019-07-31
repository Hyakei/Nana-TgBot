import requests

from nana import app, Command
from pyrogram import Filters

__MODULE__ = "Device"
__HELP__ = """
Google Drive stuff, for login just type /gdrive in Assistant bot

──「 **Download From Drive URL** 」──
-> `gdrive download`
Give url as args to download it.

──「 **Upload From local to Google Drive** 」──
-> `gdrive upload`
Upload from local storage to gdrive

──「 **Mirror and save to GDrive file** 」──
-> `gdrive mirror`
This can mirror from file download was limited, but not for deleted file

──「 **Mirror from telegram to GDrive** 」──
-> `gdrive tgmirror`
Download file from telegram, and mirror it to Google Drive
"""


DEVICE_LIST = "https://raw.githubusercontent.com/androidtrackers/certified-android-devices/master/devices.json"

@app.on_message(Filters.user("self") & Filters.command(["device"], Command))
def get_device_info(client, message):
	if len(message.text.split()) == 1:
		message.edit("Usage: `device (codename)`")
		return
	getlist = requests.get(DEVICE_LIST).json()
	targetdevice = message.text.split()[1]
	devicelist = []
	found = False
	for x in getlist:
		if x['device'].lower() == targetdevice:
			found = True
			message.edit("Brand: `{}`\nName: `{}`\nDevice: `{}`\nCodename: `{}`".format(x['brand'], x['name'], x['model'], x['device']))
			break
	if not found:
		message.edit("Device {} was not found!".format(targetdevice))
