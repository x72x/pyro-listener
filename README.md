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

### Installing

``` bash
pip3 install -U pyro-listener
```

### Community

- Join the telegram channel: https://t.me/Y88F8
