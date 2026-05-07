import asyncio
from telethon import events
from telethon.errors import FloodWaitError
from telethon.tl.custom import Message
import logging

logger = logging.getLogger(__name__)

def setup_handlers(client, from_chats, to_chats, blocked_texts, media_forward, forward_edit, delay):
    
    @client.on(events.NewMessage(chats=from_chats, incoming=True))
    async def forward_new(event: Message):
        await forward_message(event, to_chats, blocked_texts, media_forward, delay)

    if forward_edit:
        @client.on(events.MessageEdited(chats=from_chats))
        async def forward_edit(event: Message):
            await forward_message(event, to_chats, blocked_texts, media_forward, delay, is_edit=True)

async def forward_message(event, to_chats, blocked_texts, media_forward, delay, is_edit=False):
    try:
        text = (event.raw_text or "").lower()
        if any(blocked in text for blocked in blocked_texts):
            logger.info(f"Blocked message: {event.id}")
            return

        if event.media and not media_forward:
            logger.info(f"Media skipped: {event.id}")
            return

        for dest in to_chats:
            try:
                if event.grouped_id:  # Album
                    await client.forward_messages(dest, event)
                else:
                    await client.send_message(
                        dest,
                        event.message,
                        file=event.media if event.media else None,
                        formatting_entities=event.entities
                    )
                logger.info(f"{'Edited' if is_edit else 'Forwarded'} message {event.id} -> {dest}")
            except FloodWaitError as e:
                logger.warning(f"Flood wait: sleeping {e.seconds}s")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                logger.error(f"Error to {dest}: {e}")
            
            await asyncio.sleep(delay)  # Avoid rate limits

    except Exception as e:
        logger.error(f"General error forwarding {event.id}: {e}")
