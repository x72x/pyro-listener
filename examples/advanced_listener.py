from pyrogram import Client, filters, idle, types
from pyrolistener import Listener, exceptions

app = Client("name")
app.start()
listener = Listener(client=app)

@app.on_message(filters.photo)
async def _(c: Client, m: types.Message):
    await m.reply_photo(m.photo.file_id, caption="are you sure to add an button to the photo? send Y/N")
    msg = await listener.listen(
        m.chat.id,
        from_id=m.from_user.id,
        filters=["text"]
    )
    if msg.text.lower() == "y":
        return await msg.reply_photo(
            m.photo.file_id,
            reply_markup=types.InlineKeyboardMarkup(
                [[types.InlineKeyboardButton("button", "callback")]]
            )
        )
    elif msg.text.lower() == "n":
        return await msg.reply("Okay")
    else:
        return await msg.reply("Wrong choice")

print(app.me)
idle()
