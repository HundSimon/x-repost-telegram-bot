import json
import logging

from pyexpat.errors import messages
from rich.diagnose import report
from telegram import Update, InputFile, InputMedia, InputMediaPhoto
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
from modules.downloader import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

with open('config.json', 'r', encoding='utf-8') as configFile:
    config = json.load(configFile)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == config["TELEGRAM_ADMIN_ID"]:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=update.effective_chat.id
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You are not authorized to use this bot"
        )

async def repost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == config["TELEGRAM_ADMIN_ID"]:
        url = update.message.text
        username = extract_username(url)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Fetching images...",
        )
        image_urls = downloader(url)
        media_group = [InputMediaPhoto(media=url) for url in image_urls]
        await context.bot.send_media_group(
            chat_id=config["TELEGRAM_CHANNEL_ID"],
            media=media_group,
            caption=f"[Repost from @{username}]({url})",
            parse_mode="MarkdownV2"
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You are not authorized to use this bot"
        )

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.effective_chat.id
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(config["TELEGRAM_BOT_TOKEN"]).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    get_id_handler = CommandHandler("getid", get_id)
    application.add_handler(get_id_handler)

    repost_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, repost)
    application.add_handler(repost_handler)

    application.run_polling()