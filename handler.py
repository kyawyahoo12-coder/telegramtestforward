import asyncio
from telethon import events
from telethon.errors import FloodWaitError
import logging

logger = logging.getLogger(__name__)

def setup_handlers(client, from_chats, to_chats, blocked_texts, media_forward, forward_edit, delay):
    
    @client.on(events.NewMessage(chats=from_chats, incoming=True))
    async def forward_new(event):
        await forward_message(event, to_chats, blocked_texts, media_forward, delay)

    if forward_edit:
        @client.on(events.MessageEdited(chats=from_chats))
        async def forward_edited(event):
            await forward_message(event, to_chats, blocked_texts, media_forward, delay, is_edit=True)

async def forward_message(event, to_chats, blocked_texts, media_forward, delay, is_edit=False):
    try:
        # Block messages containing blocked words
        text = (event.raw_text or "").lower()
        if blocked_texts and any(blocked in text for blocked in blocked_texts):
            logger.info(f"🚫 Blocked message {event.id}")
            return

        # Skip media if disabled
        if event.media and not media_forward:
            logger.info(f"⏭️ Media skipped {event.id}")
            return

        for dest in to_chats:
            try:
                # Better way to forward albums/media groups
                await client.forward_messages(dest, event)
                status = "Edited" if is_edit else "Forwarded"
                logger.info(f"✅ {status} {event.id} → {dest}")
                
            except FloodWaitError as e:
                logger.warning(f"⏳ FloodWait: sleeping {e.seconds} seconds")
                await asyncio.sleep(e.seconds + 1)
            except Exception as e:
                logger.error(f"❌ Error forwarding to {dest}: {e}")

            await asyncio.sleep(delay)  # Rate limit protection

    except Exception as e:
        logger.error(f"General error in forward_message: {e}")
