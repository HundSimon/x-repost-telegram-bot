# x-repost-telegram-bot

Telegram bot for reposting content from other platforms.

Currently, supports reposting from: X(Twitter) & Pixiv & kemono.su

## Deployment

1. Clone the repository
```bash
git clone https://github.com/HundSimon/x-repost-telegram-bot.git
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create a new bot on the [BotFather](https://t.me/botfather) and get the API token

4. Configure the bot by editing the `config.py` file

```bash
cp config.json.example config.json
```

```bash
vim config.json
```

You can get Pixiv refresh token by using [pixiv_auth.py](https://gist.github.com/ZipFile/c9ebedb224406f4f11845ab700124362)

5. Run the bot
```bash
python main.py
```

## TODO

- [ ] Error handling
- [x] X video reposting
- [x] Pixiv multi-image reposting
- [x] e621 support
- [ ] furryaffinity support
- [ ] e-hentai support
- [x] kemono.su support