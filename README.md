<p align="center">
    <a href="https://github.com/x72x/pyro-listener/">
        <img src="https://raw.githubusercontent.com/x72x/pyro-listener/main/assest/Screenshot%202023-09-14%20212426.png" alt="pyro-listener" width="">
    </a>
    <br>
    <b>Pyrogram listener</b>
    <br>
    <a href="https://github.com/x72x/pyro-listener/tree/main/examples">
        Examples
    </a>
    •
    <a href="https://t.me/Y88F8">
        News
    </a>
</p>

## Pyrolistener

> Message listener example

``` python
from pyrogram import Client, filters, types, idle
from pyrolistener import Listener

app = Client("name")

app.start()

listener = Listener(client=app, show_output=True)

@app.on_message(filters.command("start"))
async def _(c: Client, m: types.Message):
    msg = await listener.listen_to(m, "What's your name?", filters=["text"])
    return await msg.reply(f"Your name is {msg.text}")

print("run")
idle()
```

> callbackQuery listener example
```python
@app.on_callback_query()
async def _(c: Client, query: types.CallbackQuery):
    if query.data == "name":
        msg = await listener.listen_to(
            query,
            "Whats Your name ?",
            fiilters=["text"]
        )
        return await msg.reply(f"Your Name is {msg.text}")
```

> TimeOut example
```python
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
```

> Advnced listener example
```python
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
```

> Filters type example
```python
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
```

### Installing

``` bash
pip3 install -U pyro-listener
```

### Community

- Join the telegram channel: https://t.me/Y88F8

### Examples
- https://github.com/x72x/pyro-listener/tree/main/examples
