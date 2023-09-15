from pyrogram import Client, filters, idle, types
from pyrolistener import Listener, exceptions

app = Client("name")
app.start()
listener = Listener(client=app)

@app.on_message(filters.command("start"))
async def __(c: Client, m: types.Message):
    try:
        msg = await listener.listen_to(
            m,
            "Send your name!",
            reply_markup=types.ForceReply(selective=True, placeholder="Your name"),
            filters=["text"],
            timeout=10
        )
    except exceptions.TimeOut:
        msg = None
        print("Time Out !")
        await m.reply("Time Out", quote=True)
    if msg:
        await msg.reply(f"Your name is {msg.text}", quote=True)
        # to delete client question message:
        await msg.output.delete()

print(app.me)
idle()
