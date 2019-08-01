import asyncio
import subprocess
import os
import asyncio
import requests
import time

from bs4 import BeautifulSoup
from pathlib import Path

from nana import app, Command
from pyrogram import Filters
from nana.helpers.parser import cleanhtml

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
Download and convert to music, send to tg as music.
Powered by @YTAudioBot, because no need extra bandwith in your client :p
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
		await message.edit("Write any args here!")
		return
	teks = args[1]
	balasan = "\n\nMendownload..."
	await message.edit(teks+balasan, disable_web_page_preview=True)
	await client.send_message("@YTAudioBot", teks)
	time.sleep(1)
	num = 0
	rusakin = False
	while True:
		num += 1
		await client.send_chat_action(message.chat.id, action="cancel")
		dialog = client.get_dialogs(limit=10)
		for x in dialog:
			if x['chat']['username'] == "YTAudioBot":
				if x['top_message']['reply_markup']:
					print("Done!")
					await client.request_callback_answer("@YTAudioBot", message_id=int(x['top_message']['message_id']), callback_data=x['top_message']['reply_markup']['inline_keyboard'][0][-1]['callback_data'])
					rusakin = True
		if rusakin == True:
			break
		time.sleep(1)
		if num >= 5:
			await message.edit("Can't download it!\nMaintenance maybe?")
			return
	rusakin = False
	while True:
		num += 1
		dialog = await client.get_dialogs(limit=10)
		for x in dialog:
			if x['chat']['username'] == "YTAudioBot":
				if x['top_message']['audio']:
					print("Done!")
					title = "**🎶 {}**\n".format(x['top_message']['audio']['title'])
					title += "👤 `{}`\n".format(x['top_message']['audio']['performer'])
					title += "🕘 `{}`\n".format(time.strftime('%H:%M:%S', time.gmtime(int(x['top_message']['audio']['duration']))))
					title += "🗂 `{}`\n".format(x['top_message']['audio']['mime_type'])
					title += "💾 `{} MB`".format("{0:.2f}".format(int(x['top_message']['audio']['file_size'])/1024000))
					client.send_audio(message.chat.id, audio=x['top_message']['audio']['file_id'], caption=title, parse_mode='markdown')
					rusakin = True
		if rusakin == True:
			break
		time.sleep(1)
		if num >= 8:
			await message.edit("Can't download it!\nMaintenance maybe?")
			return
	await message.delete()

