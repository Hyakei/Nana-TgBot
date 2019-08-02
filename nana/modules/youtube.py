import asyncio
import subprocess
import os
import asyncio
import requests
import logging
import time
import pafy
import re
import requests
import shutil
import subprocess
import traceback
import sys

from bs4 import BeautifulSoup
from pathlib import Path

from nana import app, setbot, Command
from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton
from nana.helpers.parser import cleanhtml, escape_markdown

__MODULE__ = "YouTube"
__HELP__ = """
Search, download, convert music from youtube!
Enjoy~

──「 **Search video** 」──
-> `youtube`
-> `yt`
Give text as args for search from youtube, will send result more than 10 depending on yt page.

──「 **Download video** 」──
-> `ytdl`
Download youtube video (mp4), you can select resolutions from the list.

──「 **Convert to music** 」──
-> `ytmusic`
-> `ytaudio`
Download youtube music, and then send to tg as music.
"""

@app.on_message(Filters.user("self") & Filters.command(["youtube", "yt"], Command))
async def youtube_search(client, message):
	args = message.text.split(None, 1)
	if len(args) == 1:
		await message.edit("Write any args here!")
		return
	teks = args[1]
	responce = requests.get('https://www.youtube.com/results?search_query=' + teks.replace(" ", "%20"))
	soup = BeautifulSoup(responce.content, "html.parser")
	divs = soup.find_all("div", {"class" : "yt-lockup"})
	yutub = "<b>Results of {}</b>\n".format(teks)
	nomor = 0
	for i in divs:
		title = cleanhtml(str(i.find('h3', {'class' :"yt-lockup-title"}).a.span))
		url = i.find('h3', {'class' :"yt-lockup-title"}).a['href']
		vidtime = i.find("span", {"class": "video-time"})
		if vidtime:
			vidtime = str("(" + cleanhtml(str(vidtime)) + ")")
		else:
			vidtime = ""
		nomor += 1
		yutub += '<b>{}.</b> <a href="{}">{}</a> {}\n'.format(nomor, "https://www.youtube.com" + url, title, vidtime)
	await message.edit(yutub, disable_web_page_preview=True, parse_mode="html")

@app.on_message(Filters.user("self") & Filters.command(["ytdl"], Command))
async def youtube_downloader(client, message):
	args = message.text.split(None, 1)
	if len(args) == 1:
		await message.edit("Write any args here!")
		return
	teks = args[1]
	await message.edit("Checking...")
	if "youtu.be" in teks:
		ytid = teks.split("youtu.be/")[1]
		if "&" in ytid:
			ytid = ytid.split("&")[0]
	elif "watch?" in teks:
		ytid = teks.split("watch?v=")[1]
		if "&" in ytid:
			ytid = ytid.split("&")[0]
	else:
		await message.edit("URL not supported!")
		return
	yt = requests.get("https://api.unblockvideos.com/youtube_downloader?id={}&selector=mp4".format(ytid)).json()
	thumb = "https://i1.ytimg.com/vi/{}/mqdefault.jpg".format(ytid)
	title = cleanhtml(str(BeautifulSoup(requests.get('https://www.youtube.com/watch?v={}'.format(ytid)).content).find('span', {"class": "watch-title"})))
	capt = "**{}**\nDownloads:".format(title)
	for x in yt:
		capt += "\n-> [{}]({})".format(x['format'], x['url'])
	try:
		await client.send_photo(message.chat.id, photo=thumb, caption=capt, reply_to_message_id=message.message_id, parse_mode='markdown')
	except:
		await message.edit(capt + "[⁣]({})".format(thumb), disable_web_page_preview=True)


@app.on_message(Filters.user("self") & Filters.command(["ytmusic", "ytaudio"], Command))
async def youtube_music(client, message):
	args = message.text.split(None, 1)
	if len(args) == 1:
		await message.edit("Send URL here!")
		return
	teks = args[1]
	balasan = "\n\nChecking..."
	try:
		video = pafy.new(teks)
	except ValueError:
		await message.edit("Invaild URL!")
		return
	try:
		audios = [audio for audio in video.audiostreams]
		audios.sort(key=lambda a: (int(a.quality.strip('k')) * -1))
		music = audios[0]
		text = "🎬 Title: [{}]({})\n".format(escape_markdown(video.title), video.watchv_url)
		text += "👤 Author: `{}`\n".format(video.author)
		text += "🕦 Duration: `{}`\n".format(video.duration)
		origtitle = re.sub(r'[\\/*?:"<>|]',"", str(music.title + "." + music._extension))
		musictitle = re.sub(r'[\\/*?:"<>|]',"", str(music.title))
		titletext = "**Downloading music...**\n"
		await message.edit(titletext+text, disable_web_page_preview=True)
		r = requests.get("https://i.ytimg.com/vi/{}/0.jpg".format(video.videoid), stream=True)
		avthumb = False
		if r.status_code == 200:
			avthumb = True
			with open("nana/cache/thumb.jpg", "wb") as stk:
				shutil.copyfileobj(r.raw, stk)
		try:
			os.remove("nana/downloads/{}".format(origtitle))
		except FileNotFoundError:
			pass
		music.download(filepath="nana/downloads/{}".format(origtitle))
		titletext = "**Converting music...**\n"
		await message.edit(titletext+text, disable_web_page_preview=True)
		try:
			if avthumb:
				subprocess.check_output(f'ffmpeg -loglevel panic -i "nana/downloads/{origtitle}" -i "nana/cache/thumb.jpg" -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata title="{musictitle}" -metadata author="{video.author}" -metadata album_artist="{video.author}" -acodec libmp3lame -aq 4 -y "nana/downloads/{musictitle}.mp3"')
			else:
				subprocess.check_output(f'ffmpeg -loglevel panic -i "nana/downloads/{origtitle}" -metadata title="{musictitle}" -metadata author="{video.author}" -metadata album_artist="{video.author}" -acodec libmp3lame -aq 4 -y "nana/downloads/{musictitle}.mp3"')
		except FileNotFoundError:
			await message.edit("You need to install ffmpeg first!\nCheck your assistant for more information!")
			await setbot.send_message(message.from_user.id, "Hello 🙂\nYou need to install ffmpeg to make audio works better, here is guide how to install it:\n\n**If you're using linux**, go to your terminal, type:\n`sudo apt install ffmpeg`\n\n**If you're using Windows**, download ffmpeg here:\n`https://ffmpeg.zeranoe.com/builds/`\nAnd then extract (if was archive), and place ffmpeg.exe to workdir (in current dir)\n\n**If you're using heroku**, type this in your workdir:\n`heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git`\nOr if you not using heroku term, follow this guide:\n1. Go to heroku.com\n2. Go to your app in heroku\n3. Change tabs/click Settings, then search for Buildpacks text\n4. Click button Add build pack, then type `https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest`\n5. Click Save changes, and you need to rebuild your heroku app to take changes!\n\nNeed help?\nGo @AyraSupport and ask there")
			return
		try:
			os.remove("nana/downloads/{}".format(origtitle))
		except FileNotFoundError:
			pass
		titletext = "**Uploading...**\n"
		await message.edit(titletext+text, disable_web_page_preview=True)
		await app.send_audio(message.chat.id, audio="nana/downloads/{}.mp3".format(musictitle))
		try:
			os.remove("nana/cache/thumb.jpg")
		except FileNotFoundError:
			pass
		titletext = "**Done! 🤗**\n"
		await message.edit(titletext+text, disable_web_page_preview=True)
	except Exception as err:
		if str(err) == "[Errno 2] No such file or directory: 'ffmpeg': 'ffmpeg'":
			await message.edit("You need to install ffmpeg first!\nCheck your assistant for more information!")
			await setbot.send_message(message.from_user.id, "Hello 🙂\nYou need to install ffmpeg to make audio works better, here is guide how to install it:\n\n**If you're using linux**, go to your terminal, type:\n`sudo apt install ffmpeg`\n\n**If you're using Windows**, download ffmpeg here:\n`https://ffmpeg.zeranoe.com/builds/`\nAnd then extract (if was archive), and place ffmpeg.exe to workdir (in current dir)\n\n**If you're using heroku**, type this in your workdir:\n`heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git`\nOr if you not using heroku term, follow this guide:\n1. Go to heroku.com\n2. Go to your app in heroku\n3. Change tabs/click Settings, then search for Buildpacks text\n4. Click button Add build pack, then type `https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest`\n5. Click Save changes, and you need to rebuild your heroku app to take changes!\n\nNeed help?\nGo @AyraSupport and ask there")
			return
		exc_type, exc_obj, exc_tb = sys.exc_info()
		errors = traceback.format_exception(etype=exc_type, value=exc_obj, tb=exc_tb)
		await message.edit("**An error has accured!**\nCheck your assistant for more information!")
		button = InlineKeyboardMarkup([[InlineKeyboardButton("🐞 Report bugs", callback_data="report_errors")]])
		await setbot.send_message(message.from_user.id, "**An error has accured!**\n```{}```".format(errors[-1]), reply_markup=button)
		logging.exception("Execution error")
