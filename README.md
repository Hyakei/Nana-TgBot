# Nana-TgBot
### Userbot + Assistant for Telegram

Q: Why need Assistant (Real bot)?
A: Because real bot will help you a lot for many things, and make user easy to use it.

```
For windows user, please use Python 3.6.7 release or Newest instead!
```


# Installation guide

This is long boring confused stuff if you new in this, please read carefully.
If you need something, just come to [@AyraSupport](https://t.me/AyraSupport) to get help.

## Create a Real Bot

1. Go to @BotFather, then type `/newbot`
2. Insert your bot **Name**, for example **My Assistant**
3. Then insert your bot **username** It must end in `bot`. for example **MyAssistantBot**.
4. Copy Token for later

## Configuration

1. Register your account API [here](https://my.telegram.org/apps)
2. Copy api_id and api_hash for config later.
3. Go to [@EmiliaHikariBot](https://t.me/EmiliaHikariBot) or [@MissRose_bot](https://t.me/MissRose_bot), and type `/id`. Copy your ID account.
4. Rename config.example.py to **confing.py** in nana folder
5. And change config like this:

```
api_id = 12345 # From guide no 2
api_hash = "123456789abcdefghijklmnopqrstuvw" # From guide no 2

ASSISTANT_BOT_TOKEN = "TOKEN" # Replace TOKEN from guide above (@BotFather)

Owner = 388576209 # From guide no 3
AdminSettings = [388576209] # From guide no 3
```

Then you ready to go next guide

## Install Requirements

Install all requirements by python, in your terminal type this:
```
pip3 install -r requirements.txt
```

## Install Database

This is required for some features, if you want to use database, follow this guide.

- Install postgresql
```
sudo apt-get update && sudo apt-get install postgresql
```

- Change user to postgres
```
sudo su - postgres
```

- Create a user, change **YOUR_USER** with you own user
```
createuser -P -s -e YOUR_USER
```

- Create a database, dont forget to change **YOUR_USER** and **YOUR_DB_NAME**
```
createdb -O YOUR_USER YOUR_DB_NAME
```

- Test your database (optional)
```
psql YOUR_DB_NAME -h YOUR_HOST YOUR_USER
```

- After create a database, your database URL should be like this
```
sqldbtype://YOUR_USER:password@localhost:5432/YOUR_DB_NAME
```

