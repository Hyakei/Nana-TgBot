import os

from nana import app, Command
from __main__ import restart_all
from pyrogram import Filters
from nana.assistant.updater import update_changelog

from git import Repo, exc


__MODULE__ = "Updater"
__HELP__ = """
You want to update latest version?
Easy, just type like bellow

──「 **Check update** 」──
-> `update`
Only check update if avaiable

──「 **Update bot** 」──
-> `update now`
Update your bot to latest version
"""

def gen_chlog(repo, diff):
	changelog = ""
	d_form = "%H:%M - %d/%m/%y"
	for cl in repo.iter_commits(diff):
		changelog += f'• [{cl.committed_datetime.strftime(d_form)}]: {cl.summary} <{cl.author}>\n'
	return changelog


OFFICIAL_BRANCH = ('master', 'dev')
REPOSITORY = "https://github.com/AyraHikari/Nana-TgBot"

@app.on_message(Filters.user("self") & Filters.command(["update"], Command))
def Updater(client, message):
	message.edit("Checking update...")
	try:
		repo = Repo()
	except exc.NoSuchPathError as error:
		message.edit(f"Update failed!\n\n**Error:**\n`directory {error} is not found`")
		return
	except exc.InvalidGitRepositoryError as error:
		message.edit(f"Update failed!\n\n**Error:**\n`directory {error} does not seems to be a git repository`")
		return
	except exc.GitCommandError as error:
		message.edit(f'"Update failed!\n\n**Error:**\n`{error}`')
		return

	brname = repo.active_branch.name
	if brname not in OFFICIAL_BRANCH:
		message.edit(f'**[UPDATER]:** Looks like you are using your own custom branch ({brname}). \
				in that case, Updater is unable to identify which branch is to be merged. \
				please checkout to any official branch')
		return

	try:
		repo.create_remote('upstream', REPOSITORY)
	except BaseException:
		pass

	upstream = repo.remote('upstream')
	upstream.fetch(brname)
	changelog = gen_chlog(repo, f'HEAD..upstream/{brname}')

	if not changelog:
		message.edit(f'Nana is up-to-date with branch **{brname}**\n')
		return

	if len(message.text.split()) != 2:
		changelog_str = f'To update latest changelog, do\n-> `update now`\n\n**New UPDATE available for [{brname}]:\n\nCHANGELOG:**\n`{changelog}`'
		if len(changelog_str) > 4096:
			message.edit("`Changelog is too big, view the file to see it.`")
			file = open("nana/cache/output.txt", "w+")
			file.write(changelog_str)
			file.close()
			client.send_document(message.chat.id, "nana/cache/output.txt", reply_to_message_id=message.message_id, caption="`Changelog file`")
			os.remove("nana/cache/output.txt")
		else:
			message.edit(changelog_str)
		return
	elif len(message.text.split()) == 2 and message.text.split()[1] == "now":
		message.edit('`New update found, updating...`')
		try:
			upstream.pull(brname)
			message.edit('Successfully Updated!\nBot is restarting...')
		except GitCommandError:
			upstream.git.reset('--hard')
			message.edit('Successfully Updated!\nBot is restarting...')
		update_changelog(changelog)
		restart_all()
	else:
		message.edit("Usage:\n-> `update` to check update\n-> `update now` to update latest commits\nFor more information check at your Assistant")
