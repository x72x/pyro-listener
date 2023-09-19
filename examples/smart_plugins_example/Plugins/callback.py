from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from config import listener

@Client.on_callback_query(filters.regex("^1$"))
async def on_callback_query(client: Client, query: CallbackQuery):
    msg = await listener.listen_to(
        m=query,
        text="What's your name?",
        filters=["text"],
        reply_to_message_id=query.message.id
    )
    # msg = await listener.listen(
    #     chat_id=query.message.chat.id,
    #     client=client, # or query._client
    #     text="What's your name?",
    #     filters=["text"],
    #     reply_to_message_id=query.message.id,
    #     from_id=query.from_user.id
    # )
    return await msg.reply(
        f"Hi {msg.text}!",
        quote=True
    )
