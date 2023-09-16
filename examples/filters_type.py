from pyrogram import Client, filters, idle, types
from pyrolistener import Listener

app = Client("name")

app.start()

listener = Listener(app)

@app.on_message(filters.command("ask") & filters.group)
async def _(c: Client, message: types.Message):
    msg = await listener.listen(
        chat_id=message.chat.id,
        text="What's your name",
        filters=["sender_chat", "text"],
        filters_type=2
    ) # will only listen to an message has "sender_chat" and "text" attribute
    msg = await listener.listen(
        chat_id=message.chat.id,
        text="What's your name",
        filters=["sender_chat", "text"],
        filters_type=1
    ) # will listen to any messgae has "sender_chat" or "text" attribute
    return await msg.reply(f"Youe name is {msg.text}")

print(app.me.first_name)
idle()
