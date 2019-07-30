import logging
import importlib

import pyrogram
from pyrogram import Filters
from nana import app, Owner, log, Command, SETTINGS_BOT, setbot

from nana.modules import ALL_MODULES
from nana.settings import ALL_SETTINGS
from nana import Load, NoLoad

app.start()
if SETTINGS_BOT:
	setbot.start()



if __name__ == '__main__':
	# Nana
	Bantuan = []
	for modul in ALL_MODULES:
		imported_module = importlib.import_module("nana.modules." + modul)
		if hasattr(imported_module, "HelpCMD") and imported_module.HelpCMD:
			Bantuan.append({"file": modul, "judul": imported_module.NamaModul, "bantuan": imported_module.HelpCMD})
	for module_name in ALL_MODULES:
		imported_module = importlib.import_module("nana.modules." + module_name)
	# Settings bot
	if SETTINGS_BOT:
		for setting in ALL_SETTINGS:
			imported_module = importlib.import_module("nana.settings." + setting)
	log.info("-----------------------")
	log.info("Modul telah dijalankan: " + str(ALL_MODULES))
	log.info("-----------------------")
	log.info("Sukses menjalankan bot!")
