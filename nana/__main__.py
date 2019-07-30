import logging
import importlib

import pyrogram
from pyrogram import Filters
from nana import app, Owner, log, Command, SETTINGS_BOT, setbot

from nana.modules import ALL_MODULES
from nana.settings import ALL_SETTINGS
from nana import Load, NoLoad


def start_userbot():
	app.start()
	for modul in ALL_MODULES:
		imported_module = importlib.import_module("nana.modules." + modul)

def start_settings():
	setbot.start()
	for setting in ALL_SETTINGS:
		imported_module = importlib.import_module("nana.settings." + setting)

if __name__ == '__main__':
	# Nana
	start_userbot()
	# Settings bot
	if SETTINGS_BOT:
		start_settings()
	log.info("-----------------------")
	log.info("Modul telah dijalankan: " + str(ALL_MODULES))
	log.info("-----------------------")
	log.info("Sukses menjalankan bot!")
