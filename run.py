import asyncio
import logging
import config

from telethon import TelegramClient

from ping import TelegramBotPing

logging.basicConfig(format="%(asctime)s [%(levelname)5s] %(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger()


async def main() -> None:
    client = TelegramClient("telegram-bot-pinger", config.API_ID, config.API_HASH)
    await client.start()

    me = await client.get_me()
    logger.info("Starting pinger with user %s", me.stringify())



asyncio.run(main())
