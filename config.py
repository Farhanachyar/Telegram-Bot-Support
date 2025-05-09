import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

SUPPORT_CHANNEL_ID = int(os.getenv("SUPPORT_CHANNEL_ID"))
DISCUSSION_GROUP_ID = int(os.getenv("DISCUSSION_GROUP_ID"))

SUPPORT_STAFF_IDS = [int(id) for id in os.getenv("SUPPORT_STAFF_IDS").split(',')]

TRACKING_FILE = "Database/message_tracking.json"
CONVERSATIONS_FILE = "Database/conversations.json"