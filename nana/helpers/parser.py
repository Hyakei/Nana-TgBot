import html
import re
import requests

def reporting(data):
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
