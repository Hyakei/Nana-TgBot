import logging
import os
import sys
import re
import requests

from pyrogram import Client
from pydrive.auth import GoogleAuth

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

USERBOT_VERSION = "0.1"
SETTINGSBOT_VERSION = "0.1"

# Version
lang_code = Config.lang_code
device_model = Config.device_model
app_version = "💝 Nana v{}".format(USERBOT_VERSION)
system_version = Config.system_version

# Must be filled
api_id = Config.api_id
api_hash = Config.api_hash

# Required for some features
Owner = Config.Owner
Command = Config.Command
OutputDownload = Config.OutputDownload
if OutputDownload[-1] != "/":
	OutputDownload = OutputDownload + "/"
log = logging.getLogger()

# APIs
thumbnail_API = Config.thumbnail_API
screenshotlayer_API = Config.screenshotlayer_API

# LOADER
USERBOT_LOAD = Config.USERBOT_LOAD
USERBOT_NOLOAD = Config.USERBOT_NOLOAD
SETTINGSBOT_LOAD = Config.SETTINGSBOT_LOAD
SETTINGSBOT_NOLOAD = Config.SETTINGSBOT_NOLOAD

DB_URL = Config.DB_URL
SETTINGS_BOT = Config.SETTINGS_BOT
SETTINGS_BOT_TOKEN = Config.SETTINGS_BOT_TOKEN
AdminSettings = Config.AdminSettings

gauth = GoogleAuth()

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


BASE = declarative_base()
SESSION = mulaisql()

if SETTINGS_BOT:
	setbot = Client("nana/session/ManageBot", api_id=api_id, api_hash=api_hash, bot_token=SETTINGS_BOT_TOKEN, workers=8)
else:
	setbot = None

app = Client("nana/session/Nana", api_id=api_id, api_hash=api_hash, app_version=app_version, device_model=device_model, system_version=system_version, lang_code=lang_code, workers=8)
