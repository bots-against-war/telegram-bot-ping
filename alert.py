import asyncio
import logging
import re
from datetime import datetime
from io import StringIO
from telebot import AsyncTeleBot

logger = logging.getLogger(__name__)


class TelegramAlertsHandler(logging.Handler):
    def __init__(self, bot: AsyncTeleBot, channel_id: int) -> None:
        super().__init__(level=logging.ERROR)
        self.bot = bot
        self.channel_id = channel_id
        self._tasks: set[asyncio.Task] = set()
        self.formatter = logging.Formatter(fmt="🏓 Telegram bot pinger alert\n\n%(name)s: %(message)s\n%(pathname)s:%(lineno)d")

    def setup(self) -> None:
        logging.getLogger().addHandler(self)

    NOT_LETTERS_RE = re.compile(r"\W+")

    async def _send_error_message(self, message: str):
        try:
            await self.bot.send_message(self.channel_id, "<pre>" + message + "</pre>", parse_mode="HTML")
        except Exception:
            try:
                body = StringIO(initial_value=message)
                exception_details_line = message.splitlines()[-1]
                filename = self.NOT_LETTERS_RE.sub("-", exception_details_line)
                filename = filename[:40]
                filename = f"{filename}-{datetime.now().isoformat(timespec='seconds')}.txt"
                await self.bot.send_document(self.channel_id, body, visible_file_name=filename)
            except Exception as e:
                print(f"Error sending alert to Telegram channel: {e!r}")
                await self.bot.send_message(self.channel_id, "⚠️ Не получилось отправить уведомление об ошибке!")

    def emit(self, record: logging.LogRecord) -> None:
        try:
            task = asyncio.get_running_loop().create_task(self._send_error_message(self.format(record)))
            self._tasks.add(task)
            task.add_done_callback(self._tasks.discard)
        except Exception as e:
            print(f"{self.__class__.__name__}: Unable to emit message, {e!r}")
