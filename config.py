from decouple import config
from telethon.sessions import StringSession

API_ID = config("API_ID", cast=int)
API_HASH = config("API_HASH")
SESSION_STRING = config("SESSION", default="")

FROM_CHATS = [int(x) for x in config("FROM_CHANNEL", cast=str).split()]
TO_CHATS = [int(x) for x in config("TO_CHANNEL", cast=str).split()]

BLOCKED_TEXTS = [x.strip().lower() for x in config("BLOCKED_TEXTS", default="", cast=str).split(",") if x.strip()]

MEDIA_FORWARD = config("MEDIA_FORWARD_RESPONSE", default="yes").lower() == "yes"
FORWARD_EDIT = config("FORWARD_EDIT", default="no").lower() == "yes"
DELAY = config("DELAY", default=0.5, cast=float)  # seconds between forwards
