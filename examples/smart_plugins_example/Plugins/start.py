from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import listener

@Client.on_message(filters.command("start") & (filters.private | filters.group))
async def on_start(client: Client, message: Message):
    # There's 2 ways to listen
    msg = await listener.listen(
        chat_id=message.chat.id,
        client=client, # or message._client ( pass this field only in smart plugins )
        text="What's your name ?",
        from_id=(message.from_user or message.sender_chat).id,
        filters=["text"],
        reply_to_message_id=message.id,
    )
    msg2 = await listener.listen_to(
        m=msg,
        text="How old are you?",
        filters=["text"],
        reply_to_message_id=msg.id
    )
    return await msg2.reply(
        f"Your name is : {msg.text}\n\nYou're {msg2.text} years old",
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Try callback listener", callback_data="1")]]
        )
    )
