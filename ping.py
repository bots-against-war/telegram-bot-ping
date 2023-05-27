import asyncio
import logging
import random
from telethon import TelegramClient, events

from dataclasses import dataclass


@dataclass
class TelegramBotPing:
    bot_username: str
    interval: float
    ping_command: str = "/start"
    ping_response_timeout: float = 15.0

    def __post_init__(self) -> None:
        self.logger = logging.getLogger(f"ping[{self.bot_username}]")

    def describe(self) -> str:
        return f"@{self.bot_username} must respond to {self.ping_command} within {self.ping_response_timeout:.3f} sec"

    async def run(self, user_client: TelegramClient) -> None:
        is_waiting_for_ping_response = False
        ping_response_received_future: asyncio.Future[None]

        @user_client.on(events.NewMessage(chats=[self.bot_username]))
        async def ping_response_handler(event: events.NewMessage) -> None:
            if not is_waiting_for_ping_response:
                self.logger.debug(f"Received {event} but we're not listening for ping response at the moment")
                return
            self.logger.info(f"Received {event}, counting as a ping response")
            ping_response_received_future.set_result(None)

        initial_delay = random.random() * self.interval
        self.logger.info(f"Sleeping initially for {initial_delay} sec")
        await asyncio.sleep(initial_delay)

        while True:
            try:
                is_waiting_for_ping_response = True
                ping_response_received_future = asyncio.Future()
                await user_client.send_message(self.bot_username, message=self.ping_command)
                try:
                    await asyncio.wait_for(ping_response_received_future, timeout=self.ping_response_timeout)
                    self.logger.info(f"Ping OK: {self.describe()}")
                except asyncio.TimeoutError:
                    self.logger.error(f"Ping condition failed: {self.describe()}")
            except Exception:
                self.logger.exception("Unexpected error performing ping, will try another time")
            finally:
                is_waiting_for_ping_response = False
                ping_response_received_future = asyncio.Future()

            self.logger.info(f"Sleeping for {self.interval} sec before next ping")
            await asyncio.sleep(self.interval)
