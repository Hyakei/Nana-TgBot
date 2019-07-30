import os, requests

from bs4 import BeautifulSoup

from nana import setbot, Owner, DB_AVAIABLE
from pyrogram import Filters


@setbot.on_message(Filters.user(Owner) & Filters.command(["start"]))
def start(client, message):
	text = "Hello {}!\n".format(message.from_user.first_name)
	text += "**Here is your current stats:**\n"
	text += "UserBot: `Running`\n"
	text += "Bot Settings: `Running`\n"
	text += "Database: `{}`".format(DB_AVAIABLE)
	message.reply(text)
