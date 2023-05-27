import os


API_HASH = os.environ["API_HASH"]
API_ID = os.environ["API_ID"]
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

BOT_TOKEN = os.environ["BOT_TOKEN"]
ALERTS_CHAT_ID = os.environ["ALERTS_CHAT_ID"]
NOTIFICATIONS_CHAT_ID = os.environ["NOTIFICATIONS_CHAT_ID"]

SILENT = bool(os.environ.get("SILENT", False))
