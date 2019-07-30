import logging
import os
import sys
import re
import requests

from pyrogram import Client

# Postgresql
import threading

from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import func, distinct, Column, String, UnicodeText, Integer

# logging
logging.basicConfig(level=logging.INFO)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error("You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting.")
    quit(1)

from nana.config import Development as Config

# Versi
lang_code = Config.lang_code
device_model = Config.device_model
app_version = Config.app_version
system_version = Config.system_version

USERBOT_VERSION = "v0.1"
SETTINGSBOT_VERSION = "v0.1"

# Dibutuhkan
api_id = Config.api_id
api_hash = Config.api_hash
Owner = Config.Owner
Load = Config.Load
NoLoad = Config.NoLoad
Command = Config.Command
OutputDownload = Config.OutputDownload
log = logging.getLogger()

DB_URL = Config.DB_URL
SETTINGS_BOT = Config.SETTINGS_BOT
SETTINGS_BOT_TOKEN = Config.SETTINGS_BOT_TOKEN
AdminSettings = Config.AdminSettings

DB_AVAIABLE = False

# Postgresql
def mulaisql() -> scoped_session:
	global DB_AVAIABLE
	engine = create_engine(DB_URL, client_encoding="utf8")
	BASE.metadata.bind = engine
	try:
		BASE.metadata.create_all(engine)
	except exc.OperationalError:
		DB_AVAIABLE = False
		return False
	DB_AVAIABLE = True
	return scoped_session(sessionmaker(bind=engine, autoflush=False))

def deldog(data):
	BASE_URL = 'https://del.dog'
	r = requests.post(f'{BASE_URL}/documents', data=data.encode('utf-8'))
	if r.status_code == 404:
		update.effective_message.reply_text('Failed to reach dogbin')
		r.raise_for_status()
	res = r.json()
	if r.status_code != 200:
		update.effective_message.reply_text(res['message'])
		r.raise_for_status()
	key = res['key']
	if res['isUrl']:
		reply = f'Shortened URL: {BASE_URL}/{key}\nYou can view stats, etc. [here]({BASE_URL}/v/{key})'
	else:
		reply = f'{BASE_URL}/{key}'
	return reply

def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext

def escape_markdown(text):
	"""Helper function to escape telegram markup symbols."""
	escape_chars = '\*_`\['
	return re.sub(r'([%s])' % escape_chars, r'\\\1', text)

def mention_html(user_id, name):
	return u'<a href="tg://user?id={}">{}</a>'.format(user_id, html.escape(name))

def mention_markdown(user_id, name):
	return u'[{}](tg://user?id={})'.format(escape_markdown(name), user_id)



BASE = declarative_base()
SESSION = mulaisql()

if SETTINGS_BOT:
	setbot = Client("nana/session/ManageBot", api_id=api_id, api_hash=api_hash, bot_token=SETTINGS_BOT_TOKEN, workers=8)
else:
	setbot = None

app = Client("nana/session/Nana", api_id=api_id, api_hash=api_hash, app_version=app_version, device_model=device_model, system_version=system_version, lang_code=lang_code, workers=8)
