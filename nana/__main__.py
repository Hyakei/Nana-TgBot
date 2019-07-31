import time
import logging
import importlib
import sys
import traceback

import pyrogram
from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton
from nana import app, Owner, log, Command, SETTINGS_BOT, setbot

from nana.modules import ALL_MODULES
from nana.settings import ALL_SETTINGS


RUNTIME = 0
HELP_COMMANDS = {}


def get_runtime():
	return RUNTIME

def reload_userbot():
	app.start()
	for modul in ALL_MODULES:
		imported_module = importlib.import_module("nana.modules." + modul)
		importlib.reload(imported_module)


def except_hook(errtype, value, tback):
	sys.__excepthook__(type, value, tback)
	errors = traceback.format_exception(etype=type, value=value, tb=tback)
	button = InlineKeyboardMarkup([[InlineKeyboardButton("🐞 Report bugs", callback_data="report_errors")]])
	text = "An error has accured!\n\n```{}```\n".format("".join(errors))
	if errtype == ModuleNotFoundError:
		text += "\nWhat should you do is: **pip install -r requirements.txt**"
	setbot.send_message(app.get_me().id, text, reply_markup=button)

sys.excepthook = except_hook



if __name__ == '__main__':
	# Nana
	app.start()
	for modul in ALL_MODULES:
		imported_module = importlib.import_module("nana.modules." + modul)
		if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
			imported_module.__MODULE__ = imported_module.__MODULE__
		if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
			if not imported_module.__MODULE__.lower() in HELP_COMMANDS:
				HELP_COMMANDS[imported_module.__MODULE__.lower()] = imported_module
			else:
				raise Exception("Can't have two modules with the same name! Please change one")
		if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
			HELP_COMMANDS[imported_module.__MODULE__.lower()] = imported_module
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
	RUNTIME = int(time.time())
