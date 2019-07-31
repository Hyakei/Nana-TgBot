import time
import datetime
import os
import pydrive
import requests
from pydrive.drive import GoogleDrive

from bs4 import BeautifulSoup
from nana import app, setbot, Command, OutputDownload, gauth
from nana.helpers.parser import cleanhtml
from pyrogram import Filters

__MODULE__ = "Google Drive"
__HELP__ = """
Download any file from URL or from telegram

──「 **Download From URL** 」──
-> `dl`
Give url as args to download it.

──「 **Download From Telegram** 」──
-> `download`
Reply a document to download it.
"""


def get_drivedir(drive):
	file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
	for drivefolders in file_list:
		if drivefolders['title'] == 'Nana Drive':
			return drivefolders['id']
	mkdir = drive.CreateFile({'title': 'Nana Drive', "mimeType": "application/vnd.google-apps.folder"})
	mkdir.Upload()

def get_driveid(driveid):
	if "http" in driveid or "https" in driveid:
		drivesplit = driveid.split('drive.google.com')[1]
		if '/d/' in drivesplit:
			driveid = drivesplit.split('/d/')[1].split('/')[0]
		elif 'id=' in drivesplit:
			driveid = drivesplit.split('id=')[1].split('&')[0]
		else:
			return False
	return driveid

def get_driveinfo(driveid):
	getdrivename = BeautifulSoup(requests.get('https://drive.google.com/uc?export=download&id={}'.format(driveid), allow_redirects=False).content)
	filename = getdrivename.find('span', {'class': 'uc-name-size'})
	if filename == None:
		filenamesize = None
		filename = None
	else:
		filenamesize = cleanhtml(str(filename))
		filename = cleanhtml(str(filename.a))
	return filename, filenamesize


@app.on_message(Filters.user("self") & Filters.command(["gdrive"], Command))
def gdrive_stuff(client, message):
	gauth.LoadCredentialsFile("nana/session/drive")
	if gauth.credentials is None:
		message.edit("You are not logged in to your google drive account!\nYour assistant boy may help you to login google drive, check your assistant bot for more information!")
		gdriveclient = os.path.isfile("client_secrets.json")
		if not gdriveclient:
			setbot.send_message(message.from_user.id, "Hello, look like you're not logged in to google drive 🙂\nI can help you to login.\n\nFirst of all, you need to activate your google drive API\n1. [Go here](https://developers.google.com/drive/api/v3/quickstart/python), click **Enable the drive API**\n2. Login to your google account (skip this if you're already logged in)\n3. After logged in, click **Enable the drive API** again, and click **Download Client Configuration** button, download that.\n4. After downloaded that file, rename `credentials.json` to `client_secrets.json`, and upload to your bot dir (not in nana dir)\n\nAfter that, you can go next guide by type /gdrive")
		else:
			setbot.send_message(message.from_user.id, "Hello, look like you're not logged in to google drive :)\nI can help you to login.\n\n**To login Google Drive**\n1. `/gdrive login` to get login URL\n2. After you're logged in, copy your Token.\n3. `/gdrive login (token)` without `(` or `)` to login, and your session will saved to `nana/session/drive`.\n\nDon't share your session to someone, else they will hack your google drive account!")
		return
	elif gauth.access_token_expired:
		# Refresh them if expired
		gauth.Refresh()
	else:
		# Initialize the saved creds
		gauth.Authorize()

	drive = GoogleDrive(gauth)
	drive_dir = get_drivedir(drive)

	if len(message.text.split()) == 3 and message.text.split()[1] == "download":
		message.edit("Downloading...")
		driveid = get_driveid(message.text.split()[2])
		if not driveid:
			message.edit("Invaild URL!\nIf you think this is bug, please go to your Assistant bot and type `/reportbug`")
			return
		filename, filenamesize = get_driveinfo(driveid)
		if not filename:
			message.edit("Invaild URL!\nIf you think this is bug, please go to your Assistant bot and type `/reportbug`")
			return
		message.edit("Downloading for `{}`\nPlease wait...".format(filenamesize))
		download = drive.CreateFile({'id': driveid})
		download.GetContentFile(filename)
		os.rename(filename, OutputDownload + filename)
		message.edit("Downloaded!\nFile saved to `{}`".format(OutputDownload + filename))
	elif len(message.text.split()) == 3 and message.text.split()[1] == "upload":
		filename = message.text.split()[2].split(None, 1)[0]
		checkfile = os.path.isfile(filename)
		if not checkfile:
			message.edit("File `{}` was not found!".format(filename))
			return
		message.edit("Uploading `{}`...".format(filename))
		upload = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": drive_dir}], 'title': filename})
		upload.SetContentFile(filename)
		upload.Upload()
		upload.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
		message.edit("Uploaded!\nDownload link: [{}]({})\nDirect download link: [{}]({})".format(filename, upload['alternateLink'], filename, upload['downloadUrl']))
	elif len(message.text.split()) == 3 and message.text.split()[1] == "mirror":
		message.edit("Mirroring...")
		driveid = get_driveid(message.text.split()[2])
		if not driveid:
			message.edit("Invaild URL!\nIf you think this is bug, please go to your Assistant bot and type `/reportbug`")
			return
		filename, filenamesize = get_driveinfo(driveid)
		if not filename:
			message.edit("Invaild URL!\nIf you think this is bug, please go to your Assistant bot and type `/reportbug`")
			return
		mirror = drive.auth.service.files().copy(fileId=driveid, body={"parents": [{"kind": "drive#fileLink", "id": drive_dir}], 'title': filename}).execute()
		new_permission = {'type': 'anyone', 'value': 'anyone', 'role': 'reader'}
		drive.auth.service.permissions().insert(fileId=mirror['id'], body=new_permission).execute()
		message.edit("Done!\nDownload link: [{}]({})\nDirect download link: [{}]({})".format(filename, mirror['alternateLink'], filename, mirror['downloadUrl']))
	elif len(message.text.split()) == 2 and message.text.split()[1] == "tgmirror":
		if message.reply_to_message:
			message.edit("__Downloading...__")
			if message.reply_to_message.photo:
				nama = "photo_{}_{}.png".format(message.reply_to_message.photo.id, message.reply_to_message.photo.date)
				client.download_media(message.reply_to_message.photo.file_id, file_name=OutputDownload + nama)
			elif message.reply_to_message.animation:
				nama = "giphy_{}-{}.gif".format(message.reply_to_message.animation.date, message.reply_to_message.animation.file_size)
				client.download_media(message.reply_to_message.animation.file_id, file_name=OutputDownload + nama)
			elif message.reply_to_message.video:
				nama = "video_{}-{}.mp4".format(message.reply_to_message.video.date, message.reply_to_message.video.file_size)
				client.download_media(message.reply_to_message.video.file_id, file_name=OutputDownload + nama)
			elif message.reply_to_message.sticker:
				nama = "sticker_{}_{}.webp".format(message.reply_to_message.sticker.date, message.reply_to_message.sticker.set_name)
				client.download_media(message.reply_to_message.sticker.file_id, file_name=OutputDownload + nama)
			elif message.reply_to_message.audio:
				nama = "{}".format(message.reply_to_message.audio.file_name)
				client.download_media(message.reply_to_message.audio.file_id, file_name=OutputDownload + nama)
			elif message.reply_to_message.voice:
				nama = "audio_{}.ogg".format(message.reply_to_message.voice.file_id)
				client.download_media(message.reply_to_message.voice.file_id, file_name=OutputDownload + nama)
			elif message.reply_to_message.document:
				nama = "{}".format(message.reply_to_message.document.file_name)
				client.download_media(message.reply_to_message.document.file_id, file_name=OutputDownload + nama)
			else:
				message.edit("Unknown file!")
				return
			upload = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": drive_dir}], 'title': nama})
			upload.SetContentFile(OutputDownload + nama)
			upload.Upload()
			upload.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
			message.edit("Done!\nDownload link: [{}]({})\nDirect download link: [{}]({})".format(nama, upload['alternateLink'], nama, upload['downloadUrl']))
			os.remove(OutputDownload + nama)
		else:
			message.edit("Reply document to mirror it to gdrive")
	else:
		message.edit("Usage:\n-> `gdrive download <url/gid>`\n-> `gdrive upload <file>`\n-> `gdrive mirror <url/gid>`\n\nFor more information about this, go to your assistant.")
		return
