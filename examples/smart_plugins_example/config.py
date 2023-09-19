from pyrogram import Client
from pyrolistener import Listener

app = Client(
    "name",
    plugins={"root":"Plugins"}
)
listener = Listener(app)
