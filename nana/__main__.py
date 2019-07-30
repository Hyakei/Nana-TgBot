import logging
import importlib

import pyrogram
from pyrogram import Filters
from nana import app, Owner, log, Command, SETTINGS_BOT, setbot

from nana.modules import ALL_MODULES
from nana.settings import ALL_SETTINGS


def reload_userbot():
	app.start()
	for modul in ALL_MODULES:
		imported_module = importlib.import_module("nana.modules." + modul)
		importlib.reload(imported_module)


if __name__ == '__main__':
	# Nana
	app.start()
	for modul in ALL_MODULES:
		imported_module = importlib.import_module("nana.modules." + modul)
	# Settings bot
	if SETTINGS_BOT:
		setbot.start()
		for setting in ALL_SETTINGS:
			imported_module = importlib.import_module("nana.settings." + setting)
	log.info("-----------------------")
	log.info("Userbot modules: " + str(ALL_MODULES))
	log.info("-----------------------")
	log.info("Settings bot modules: " + str(ALL_SETTINGS))
	log.info("-----------------------")
	log.info("Sukses menjalankan bot!")
