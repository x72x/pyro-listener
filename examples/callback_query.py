from pyrogram import Client, filters, types, idle
from pyrolistener import Listener

app = Client("name")

app.start()

listener = Listener(client=app, show_output=True)

@app.on_message(filters.command("start"))
async def _(c: Client, m: types.Message):
    await m.reply(
        "Choose :",
        reply_markup=types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton("Enter name", callback_data="name"),
                    types.InlineKeyboardButton("Enter age", callback_data="age")
                ],
            ]
        ),
        quote=True
    )

@app.on_callback_query()
async def __(c: Client, m: types.CallbackQuery):
    if m.data == "name":
        msg = await listener.listen_to(
            m,
            "Send your name now",
            filters=["text"]
        )
        return await msg.reply(f"Your name is : {msg.text}")

    if m.data == "age":
        msg = await listener.listen_to(
            m,
            "Send your age now",
            filters=["text"]
        )
        return await msg.reply(f"Your age is : {msg.text}")
# print(app.me)
print("run")
idle()
