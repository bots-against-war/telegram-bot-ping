import abc
from dataclasses import dataclass
from typing import Optional
from telebot import AsyncTeleBot

from ping import TelegramBotPing


class AlertReporter(abc.ABC):
    @abc.abstractmethod
    async def report_failure(self, failed_ping: TelegramBotPing) -> None:
        pass

    @abc.abstractmethod
    async def report_success(self, ok_ping: TelegramBotPing) -> None:
        pass


@dataclass
class TelegramChannelAlertReporter(AlertReporter):
    bot: AsyncTeleBot
    alert_channel_id: int
    ok_channel_id: Optional[int]

    async def report_failure(self, failed_ping: TelegramBotPing) -> None:
        await self.bot.send_message(chat_id=self.alert_channel_id, text=f"🏓 Ping condition failed: {failed_ping.describe()}")

    async def report_success(self, ok_ping: TelegramBotPing) -> None:
        if self.ok_channel_id is not None:
            await self.bot.send_message(chat_id=self.ok_channel_id, text=f"🏓 Ping OK: {ok_ping.describe()}")
