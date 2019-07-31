import json
import requests
import datetime
import os
import re
import shutil
import subprocess
import sys
import traceback

from nana import app, Command, logging
from nana.helpers.deldog import deldog
from nana.helpers.parser import mention_markdown
from pyrogram import Filters

__MODULE__ = "Devs"
__HELP__ = """
This command means for helping development

──「 **Execution** 」──
-> `exec`
Execute a python commands.

──「 **Evaluation** 」──
-> `eval`
Do math evaluation.

──「 **Command shell** 」──
-> `cmd`
Execute command shell

──「 **Take log** 」──
-> `log`
Edit log message, or deldog instead

──「 **Get Data Center** 」──
-> `dc`
Get user specific data center
"""


def stk(chat, photo):
	if "http" in photo:
		r = requests.get(photo, stream=True)
		with open("nana/cache/stiker.png", "wb") as stk:
			shutil.copyfileobj(r.raw, stk)
		app.send_sticker(chat, "nana/cache/stiker.png")
		os.remove("nana/cache/stiker.png")
	else:
		app.send_sticker(chat, photo)

def vid(chat, video, caption=None):
	app.send_video(chat, video, caption)

def pic(chat, photo, caption=None):
	app.send_photo(chat, photo, caption)


@app.on_message(Filters.user("self") & Filters.command(["exec"], Command))
def executor(c, m):
	if len(m.text.split()) == 1:
		message.edit("Usage: `exec m.edit('edited!')`")
		return
	args = m.text.split(None, 1)
	code = args[1]
	chat = m.chat.id
	try:
		exec(code)
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		errors = traceback.format_exception(etype=exc_type, value=exc_obj, tb=exc_tb)
		m.edit("**Execute**\n`{}`\n\n**Failed:**\n```{}```".format(code, errors[-1]))
		logging.exception("Execution error")

@app.on_message(Filters.user("self") & Filters.command(["eval"], Command))
def evaluation(client, message):
	if len(m.text.split()) == 1:
		message.edit("Usage: `eval 1000-7`")
		return
	q = message.text.split(None, 1)[1]
	try:
		ev = str(eval(q))
		if ev:
			if len(ev) >= 4096:
				file = open("output.txt", "w+")
				file.write(ev)
				file.close()
				client.send_file(message.chat.id, "output.txt", caption="`Output too large, sending as file`")
				remove("output.txt")
				return
			else:
				message.edit("**Query:**\n{}\n\n**Result:**\n`{}`".format(q, ev))
				return
		else:
			message.edit("**Query:**\n{}\n\n**Result:**\n`None`".format(q))
			return
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		errors = traceback.format_exception(etype=exc_type, value=exc_obj, tb=exc_tb)
		m.edit("Error: `{}`".format(code, errors[-1]))
		logging.exception("Evaluation error")


@app.on_message(Filters.user("self") & Filters.command(["cmd"], Command))
def terminal(client, message):
	if len(message.text.split()) == 1:
		message.edit("Usage: `cmd ping -c 5 google.com`")
		return
	args = message.text.split(None, 1)
	teks = args[1]
	if "\n" in teks:
		code = teks.split("\n")
		output = ""
		for x in code:
			shell = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', x)
			try:
				process = subprocess.Popen(
					shell,
					stdout=subprocess.PIPE,
					stderr=subprocess.PIPE
				)
			except Exception as err: 
				message.edit("""
**Input:**
```{}```

**Error:**
```{}```
""".format(teks, err))
			output += "**{}**\n".format(code)
			output += process.stdout.read()[:-1].decode("utf-8")
			output += "\n"
	else:
		shell = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', teks)
		for a in range(len(shell)):
			shell[a] = shell[a].replace('"', "")
		try:
			process = subprocess.Popen(
				shell,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
			)
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			errors = traceback.format_exception(etype=exc_type, value=exc_obj, tb=exc_tb)
			message.edit("""**Input:**\n```{}```\n\n**Error:**\n```{}```""".format(teks, errors[-1]))
			return
		output = process.stdout.read()[:-1].decode("utf-8")
	if str(output) == "\n":
		output = None
	if output:
		if len(output) > 4096:
			file = open("nana/cache/output.txt", "w+")
			file.write(output)
			file.close()
			client.send_document(message.chat.id, "nana/cache/output.txt", reply_to_message_id=message.message_id, caption="`Output file`")
			os.remove("nana/cache/output.txt")
			return
		message.edit("""**Input:**\n```{}```\n\n**Output:**\n```{}```""".format(teks, output))
	else:
		message.edit("**Input: **\n`{}`\n\n**Output: **\n`No Output`".format(teks))

@app.on_message(Filters.user("self") & Filters.command(["log"], Command))
def log(client, message):
	try:
		message.edit(str(message), parse_mode="")
	except:
		data = deldog(str(message))
		message.edit(data)

@app.on_message(Filters.user("self") & Filters.command(["dc"], Command))
def dc_id(client, message):
	chat = message.chat
	user = message.from_user
	if message.reply_to_message:
		if message.reply_to_message.forward_from:
			dc_id = client.get_user_dc(message.reply_to_message.forward_from.id)
			user = mention_markdown(message.reply_to_message.forward_from.id, message.reply_to_message.forward_from.first_name)
		else:
			dc_id = client.get_user_dc(message.reply_to_message.from_user.id)
			user = mention_markdown(message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name)
	else:
		dc_id = client.get_user_dc(message.from_user.id)
		user = mention_markdown(message.from_user.id, message.from_user.first_name)
	if dc_id == 1:
		text = "{}'s assigned datacenter is **DC1**, located in **MIA, Miami FL, USA**".format(user)
	elif dc_id == 2:
		text = "{}'s assigned datacenter is **DC2**, located in **AMS, Amsterdam, NL**".format(user)
	elif dc_id == 3:
		text = "{}'s assigned datacenter is **DC3**, located in **MIA, Miami FL, USA**".format(user)
	elif dc_id == 4:
		text = "{}'s assigned datacenter is **DC4**, located in **AMS, Amsterdam, NL**".format(user)
	elif dc_id == 5:
		text = "{}'s assigned datacenter is **DC5**, located in **SIN, Singapore, SG**".format(user)
	else:
		text = "{}'s assigned datacenter is **Unknown**".format(user)
	message.edit(text)
