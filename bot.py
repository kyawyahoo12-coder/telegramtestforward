import asyncio
import logging
from telethon import TelegramClient
from telethon.errors import FloodWaitError
import sys
import signal

from config import (
    API_ID, API_HASH, SESSION_STRING,
    FROM_CHATS, TO_CHATS, BLOCKED_TEXTS,
    MEDIA_FORWARD, FORWARD_EDIT, DELAY
)
from handler import setup_handlers

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def main():
    await client.start()
    logger.info("Bot started successfully!")
    
    setup_handlers(client, FROM_CHATS, TO_CHATS, BLOCKED_TEXTS, MEDIA_FORWARD, FORWARD_EDIT, DELAY)
    
    await client.run_until_disconnected()

if __name__ == "__main__":
    # Graceful shutdown
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(client.disconnect()))
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
