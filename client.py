from telethon.sync import TelegramClient, events
from telethon.utils import get_display_name
import logging

# Logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function helper 

def sprint(string, *args, **kwargs):
    """Safe Print (handle UnicodeEncodeErrors on some terminals)"""
    try:
        print(string, *args, **kwargs)
    except UnicodeEncodeError:
        string = string.encode('utf-8', errors='ignore')\
                       .decode('ascii', errors='ignore')
        print(string, *args, **kwargs)

# API LOGIN

# Devi prendere i tuoi da my.telegram.org
api_id = 12345678 
api_hash = 'dbccdef98793591234567'

with TelegramClient('name', api_id, api_hash) as client:
    
    client.found_media = {}

    # Rispondo quando riconosco un certo pattern

    # @client.on(events.NewMessage(pattern='(?i).*start'))
    # async def handler(event):
    #    await event.reply('Avviato!')


    @client.on(events.NewMessage(chats=-99994xxxx9098)) # CHAT ID DA FILTRARE
    async def handler(event):
        dialogs = await client.get_dialogs()

        for i, dialog in enumerate(dialogs, start=1):
            if dialog.name == 'ChannelViewerBot':
                entity = dialog.entity

        messages = await client.get_messages(entity, limit=10)
        
        for msg in reversed(messages):

            name = get_display_name(msg.sender)

            # Format the message content
            if getattr(msg, 'media', None):
                client.found_media[msg.id] = msg
                content = '<{}> {}'.format(
                    type(msg.media).__name__, msg.message)

            elif hasattr(msg, 'message'):
                content = msg.message
            elif hasattr(msg, 'action'):
                content = str(msg.action)
            else:
                # Unknown message, simply print its class name
                content = type(msg).__name__

            # Printo il messaggio
            sprint('[{}:{}] (ID={}) {}: {}'.format(
                msg.date.hour, msg.date.minute, msg.id, name, content))
            
            # print(msg.message)
        

    # Info utili: https://docs.telethon.dev/en/latest/modules/events.html#telethon.events.messageread.MessageRead
    
    client.run_until_disconnected()
