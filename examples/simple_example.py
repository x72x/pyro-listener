from pyrogram import Client, filters, types, idle
from pyrolistener import Listener

app = Client("name")

app.start()

listener = Listener(client=app, show_output=True)

@app.on_message(filters.command("start"))
async def _(c: Client, m: types.Message):
    msg = await listener.listen(
        chat_id=m.chat.id,
        text="Send you name",
        reply_to_message_id=m.id,
        filters=["text"]
    )
    return await msg.reply(f"Hi {msg.text}")

print("run")
idle()
