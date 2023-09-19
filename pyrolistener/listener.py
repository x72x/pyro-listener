import json
import pyrogram
from time import sleep
from typing import List, Union
from datetime import datetime, timedelta

from pyrogram.handlers import MessageHandler
from .exceptions import TimeOut

_cache = {}

available_filters = [
    "text", "document", "animation", "sticker", "photo", "video",
    "contact", "location", "voice", "video_note", "venue", "dice",
    "poll", "audio"
]

class Listener:
    def __init__(self, client: pyrogram.Client, show_output: bool = True) -> None:
        """
        Args:
            client (pyrogram.Client): Pyrogram Client
            show_output (bool, optional): Insert 'output' attribute to question message. Defaults to True.
        """
        super().__init__()

        self.client = client
        self.show_output = show_output
        _cache[client.name]={}
        _cache[client.name]['list']=[]

        self.client.add_handler(MessageHandler(self._handler), group=-99)

    async def listen(
        self,
        chat_id: int,
        client: pyrogram.Client = None,
        text: str = None,
        from_id: Union[List[int], int] = None,
        filters: List[str] = available_filters,
        filters_type: int = 1,
        protect_content: bool = None,
        reply_to_message_id: int = None,
        disable_web_page_preview: bool = True,
        timeout: int = None,
        parse_mode=None,
        reply_markup=None,
    ) -> pyrogram.types.Message:
        """

        Args:
            chat_id (int): chat id
            client (pyrogram.Client, optional): Pyrogram Client for Smart Plugins. Default to main client.
            text (str, optional): Defaults to None.
            from_id (Union[List[int], int], optional): peer id filters. Defaults to None.
            filters (List[str], optional): list of Message attributes. Defaults to available_filters.
            filters_type (int, optional): 1: The client will listen to any message contain one of filters, 2: The client will listen to message contain all of filters. Defaults to 1.
            protect_content (bool, optional): Defaults to None.
            reply_to_message_id (int, optional): Defaults to None.
            disable_web_page_preview (bool, optional): Defaults to True.
            timeout (int, optional): Time out. Defaults to None.
            parse_mode (optional): Defaults to None.
            reply_markup (optional): Defaults to None.

        Raises:
            TimeOut

        Returns:
            pyrogram.types.Message:
        """
        data = {
                "from_id": from_id,
                "filters": filters,
                "chat_id": chat_id,
                "filters_type": filters_type
        }
        if data in _cache[self.client.name]['list']: _cache[self.client.name]['list'].remove(data)
        _cache[self.client.name]['list'].append(data)
        if text:
            m = await (client or self.client).send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup,
                reply_to_message_id=reply_to_message_id,
                disable_web_page_preview=disable_web_page_preview,
                protect_content=protect_content,
                parse_mode=parse_mode,
            )
        else:
            m = None
        _cache[self.client.name][json.dumps(data, ensure_ascii=False)]=m
        if timeout:
            stamp = (datetime.now() + timedelta(seconds=timeout))
        else:
            stamp = None
        def ___():
            while data in _cache[self.client.name]['list']:
                if (timeout) and (datetime.now() > stamp):
                    del _cache[self.client.name][json.dumps(data, ensure_ascii=False)]
                    _cache[self.client.name]['list'].remove(data)
                    raise TimeOut("Time out error")
                sleep(0)
            return _cache[self.client.name][json.dumps(data, ensure_ascii=False)]
        return await client.loop.run_in_executor(None, ___)

    async def listen_to(self, m: Union[pyrogram.types.CallbackQuery, pyrogram.types.Message], text : str = None,*args, **kwargs):
        if isinstance(m, pyrogram.types.CallbackQuery):
            chat_id = m.message.chat.id
            from_id = m.from_user.id
            # reply_to_message_id = None
        elif isinstance(m, pyrogram.types.Message):
            chat_id = m.chat.id
            from_id = (m.from_user or m.sender_chat).id
            # reply_to_message_id = m.id
        return await self.listen(chat_id=chat_id, client=m._client, from_id=from_id, text=text, *args, **kwargs)

    async def _handler(self, client: pyrogram.Client, message: pyrogram.types.Message):
            sender = message.sender_chat or message.from_user
            chat_id = message.chat.id
            __ = []
            for data in _cache[self.client.name]['list']:
                if (data['chat_id'] == chat_id) and (
                    (data["from_id"] is None) or (isinstance(data["from_id"], list) and sender.id in data["from_id"]) or (
                        isinstance(data["from_id"], int) and data["from_id"] == sender.id
                    )
                ):
                    if data["filters_type"] == 1:
                        for _ in data["filters"]:
                            if hasattr(message, _) and getattr(message, _):
                                __.append(_)
                                break
                        if not __:
                            return False

                    if data["filters_type"] == 2:
                        for _ in data["filters"]:
                            if hasattr(message, _) and getattr(message, _):
                                __.append(_)
                        if __ != data["filters"]:
                            return False
                    if self.show_output:
                        message.output = _cache[self.client.name][json.dumps(data, ensure_ascii=False)]
                    _cache[self.client.name][json.dumps(data, ensure_ascii=False)]=message
                    _cache[self.client.name]['list'].remove(data)
