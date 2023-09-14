import json
import pyrogram
from time import sleep
from typing import List, Union
from datetime import datetime, timedelta

from pyrogram.handlers import MessageHandler
from .exceptions import ClientNotStartedYet, ClientAlreadyConnected, TimeOut

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

        Raises:
            ClientNotStartedYet
            ClientAlreadyConnected
        """
        super().__init__()

        if not client.is_connected:
            raise ClientNotStartedYet(f"Client [ {client.name} ] Not started yet")

        if client.name in _cache:
            raise ClientAlreadyConnected(f"Client [ {client.name} ] Already connected")

        _cache[client.name]={}
        _cache[client.name]['list']=[]
        self.client = client
        self.show_output = show_output
        self.client.add_handler(MessageHandler(self._handler), group=-99)

    async def listen(
        self,
        chat_id: int,
        text: str,
        from_id: int = None,
        protect_content: bool = None,
        reply_to_message_id: int = None,
        filters: List[str] = available_filters,
        disable_web_page_preview: bool = True,
        timeout: int = None,
        parse_mode=None,
        reply_markup=None,
    ) -> pyrogram.types.Message:
        """
        Args:
            chat_id (int): Chat ID
            from_id (int, optional): Only listening from specific user or sender chat. Defaults to None.
            text (str): The question.
            protect_content (bool, optional): Protect message content. Defaults to None.
            reply_to_message_id (int, optional): message to reply. Defaults to None.
            content_filters (List[str], optional): List of filters like: ['text', 'photo'] ( Message type attributes ). Defaults to None.
            disable_web_page_preview (bool, optional): Defaults to True.
            parse_mode (pyrogram.enums.ParseMode, optional): Defaults to None.
            reply_markup (optional): Defaults to None.

        Returns:
            pyrogram.types.Message: Message type, with 'output' attribute when you set show_output as True
        """
        data = {
                "from_id": from_id,
                "filters": filters,
                "chat_id": chat_id,
        }
        if data in _cache[self.client.name]['list']: _cache[self.client.name]['list'].remove(data)
        _cache[self.client.name]['list'].append(data)
        m = await self.client.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup,
                reply_to_message_id=reply_to_message_id,
                disable_web_page_preview=disable_web_page_preview,
                protect_content=protect_content,
                parse_mode=parse_mode,
        )
        _cache[self.client.name][json.dumps(data, ensure_ascii=False)]=m
        if timeout:
            stamp = timedelta(seconds=timeout)
        def ___(data, timeout):
            while data in _cache[self.client.name]['list']:
                if timeout:
                    if datetime.now().timestamp() > stamp:
                        raise TimeOut("Time out error")
                sleep(0)
            # print(_cache_[f"{m.id}|{m.chat.id}"])
            return _cache[self.client.name][json.dumps(data, ensure_ascii=False)]
        return await self.client.loop.run_in_executor(None, ___, data, timeout)

    async def listen_to(self, m: Union[pyrogram.types.CallbackQuery, pyrogram.types.Message], text : str, *args, **kwargs):
        if isinstance(m, pyrogram.types.CallbackQuery):
            chat_id = m.message.chat.id
            from_id = m.from_user.id
        elif isinstance(m, pyrogram.types.Message):
            chat_id = m.chat.id
            from_id = m.from_user.id
        return await self.listen(chat_id=chat_id, from_id=from_id, text=text,*args, **kwargs)

    async def _handler(self, client: pyrogram.Client, message: pyrogram.types.Message):
            sender = message.sender_chat or message.from_user
            chat_id = message.chat.id
            __ = []
            for data in _cache[self.client.name]['list']:
                if (data['chat_id'] == chat_id) and (data['from_id'] == sender.id):
                    for _ in data["filters"]:
                        if getattr(message, _):
                            __.append(_)
                    if not __:
                        return False
                    if self.show_output:
                        message.output = _cache[self.client.name][json.dumps(data, ensure_ascii=False)]
                    _cache[self.client.name][json.dumps(data, ensure_ascii=False)]=message
                    _cache[self.client.name]['list'].remove(data)