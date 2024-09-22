import logging

from telegram import Update, InputMediaPhoto, InputMediaVideo
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler

from modules.downloader import *
from modules.utils import convert_special_chars, get_media_type

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Load configuration from JSON file
try:
    with open('config.json', 'r', encoding='utf-8') as configFile:
        config = json.load(configFile)
except FileNotFoundError:
    logging.error("Configuration file 'config.json' not found.")
    exit(1)
except json.JSONDecodeError:
    logging.error("Error decoding JSON from 'config.json'.")
    exit(1)


# Handler functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
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
    except Exception as e:
        logging.error(f"Error in start command: {e}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"An error occurred while processing your request: {e}"
        )


async def repost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.effective_user.id == config["TELEGRAM_ADMIN_ID"]:
            url = update.message.text
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Fetching images..."
            )

            image_urls, username = downloader(url)
            media_group = []

            for _url in image_urls:
                media_type = get_media_type(_url)
                if media_type == "image":
                    media_group.append(InputMediaPhoto(media=_url))
                elif media_type == "video":
                    media_group.append(InputMediaVideo(media=_url))
                elif media_type == "unknown":
                    logging.warning(f"Unknown media type for URL: {_url}")

            await context.bot.send_media_group(
                chat_id=config["TELEGRAM_CHANNEL_ID"],
                media=media_group,
                caption=f"[Repost from @{convert_special_chars(username)}]({url})",
                parse_mode="MarkdownV2"
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="You are not authorized to use this bot"
            )
    except Exception as e:
        logging.error(f"Error in repost command: {e}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"An error occurred while processing your request: {e}"
        )


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=update.effective_chat.id
        )
    except Exception as e:
        logging.error(f"Error in get_id command: {e}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"An error occurred while processing your request: {e}"
        )


# Main entry point
if __name__ == '__main__':
    try:
        application = ApplicationBuilder().token(config["TELEGRAM_BOT_TOKEN"]).build()

        # Command handlers
        start_handler = CommandHandler('start', start)
        application.add_handler(start_handler)

        get_id_handler = CommandHandler("getid", get_id)
        application.add_handler(get_id_handler)

        # Repost handler for text messages
        repost_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, repost)
        application.add_handler(repost_handler)

        # Run the bot
        application.run_polling()
    except Exception as e:
        logging.error(f"Error starting the bot: {e}")
