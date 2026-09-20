from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 37531523
api_hash = "b4a9ecb2c20a09c26c1e1bdc110427c2"

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())