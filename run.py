import asyncio
import time
from telebot import AsyncTeleBot
import json
import logging
import pathlib
import sys
from alert import TelegramAlertsHandler
import config

from telethon import TelegramClient

from ping import TelegramBotPing

logging.basicConfig(format="%(asctime)s [%(levelname)5s] %(name)s: %(message)s", level=config.LOG_LEVEL)
logger = logging.getLogger()


async def main() -> None:
    bot = AsyncTeleBot(config.BOT_TOKEN)
    telegram_alerts_log_handler = TelegramAlertsHandler(
        bot=bot,
        channel_id=int(config.ALERTS_CHAT_ID),
    )
    telegram_alerts_log_handler.setup()

    pings_json_file = sys.argv[1]
    pings_json_raw = json.loads(pathlib.Path(pings_json_file).read_text())
    logger.info("Parsing pings from raw data: %s", pings_json_raw)
    pings = [TelegramBotPing(**raw) for raw in pings_json_raw]

    try:
        client = TelegramClient("telegram-bot-pinger", config.API_ID, config.API_HASH)
        await client.start()

        me = await client.get_me()
        logger.info("Starting pings with user %s", me.stringify())

        if not config.SILENT:
            await bot.send_message(
                config.NOTIFICATIONS_CHAT_ID,
                f"🏓 Starting Telegram bot pinger with {len(pings)} pings:\n\n<code>"
                + "\n".join(p.describe() for p in pings)
                + "</code>",
                parse_mode="HTML",
            )

        tasks = [asyncio.create_task(ping.run(client)) for ping in pings]
        await asyncio.gather(*tasks)
    finally:
        if not config.SILENT:
            logger.error("Telegram bot pinger going offline!")
        await asyncio.sleep(10)
        logger.info("Finally, dying")


asyncio.run(main())
