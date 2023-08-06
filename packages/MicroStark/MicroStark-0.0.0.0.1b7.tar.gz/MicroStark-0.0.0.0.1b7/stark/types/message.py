# MicroStark - Python add-on extension to Pyrogram
# Copyright (C) 2022 Stark Bots <https://github.com/StarkBotsIndustries>
#
# This file is part of MicroStark.
#
# MicroStark is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MicroStark is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MicroStark. If not, see <https://www.gnu.org/licenses/>.

import os
import asyncio
from .user import User
from .chat import Chat
from ..client import Stark
from stark.utils.patch import patch
from pyrogram.enums import ParseMode
from pyrogram.errors import MessageTooLong
from pyrogram.types import Message, MessageEntity


@patch(Message)
class Message(Message):
    _client: Stark
    from_user: User
    chat: Chat

    async def tell(
        self,
        text: str,
        format: str | tuple = None,
        del_in: int = 0,
        quote: bool = True,
        parse_mode: ParseMode = ParseMode.DEFAULT,
        entities: list["MessageEntity"] = None,
        disable_web_page_preview: bool = True,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        schedule_date: int = None,
        reply_markup=None
    ) -> "Message":
        try:
            if self.from_user.is_self:
                reply = await self.edit(
                    str(text),
                    parse_mode=parse_mode,
                    entities=entities,
                    disable_web_page_preview=disable_web_page_preview,
                    reply_markup=reply_markup,
                )
            else:
                reply = await self.reply(
                    str(text),
                    quote=quote,
                    parse_mode=parse_mode,
                    entities=entities,
                    disable_notification=disable_notification,
                    reply_to_message_id=reply_to_message_id,
                    schedule_date=schedule_date,
                    disable_web_page_preview=disable_web_page_preview,
                    reply_markup=reply_markup,
                )
        except MessageTooLong:
            reply = await self.reply(
                "Sending as document...",
                quote=quote,
                parse_mode=parse_mode,
                entities=entities,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                schedule_date=schedule_date,
                disable_web_page_preview=disable_web_page_preview,
                reply_markup=reply_markup,
            )
            file = f'{reply.message_id}.txt'
            with open(file, 'w+', encoding="utf-8") as f:
                f.write(text)
            await reply.delete()
            reply = await self.reply_document(
                document=file,
                caption="Output",
                quote=quote,
                parse_mode=parse_mode,
                caption_entities=entities,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                schedule_date=schedule_date,
                reply_markup=reply_markup,
            )
            os.remove(file)
        if del_in:
            await asyncio.sleep(del_in)
            await reply.delete()
        return reply

    @property
    def args(self, split: str = " ") -> list[str]:
        """List arguments passed in a message. Removes first word (the command itself)"""
        args: list[str] = self.text.markdown.split(split)
        args.pop(0)
        if args:
            args[0] = args[0].strip()
            if "\n" in args[0]:
                wtf = args[0]
                f, s = wtf.split("\n", 1)
                args[0] = f
                args.insert(1, s)
        return args

    @property
    def input(self) -> str | None:
        """Input passed in a message. Removes first word (the command itself)"""
        i = self.text.markdown.split(" ", 1)
        if len(i) > 1 and i[1]:
            return i[1]
        return

    @property
    def ref(self) -> int | str | None:
        """Returns the referred user's id or username. To get the full user, use method `get_ref_user`"""
        if self.reply_to_message:
            return self.reply_to_message.from_user.id
        args = self.args
        if not args:
            return
        return args[0] if not args[0].isdigit() else int(args[0])

    async def get_ref_user(self) -> User | None:
        """Returns the full referred user. To get only user id or username, use property `ref` as it's faster."""
        if self.reply_to_message:
            return self.reply_to_message.from_user
        args = self.args
        if not args:
            return
        user = args[0] if not args[0].isdigit() else int(args[0])
        user = await self._client.get_users(user)
        return user

    async def get_ref_chat(self) -> Chat | None:
        args = self.args
        if not args:
            return
        chat = args[0] if not args[0].isdigit() else int(args[0])
        chat = await self._client.get_chat(chat)
        return chat

    async def get_aor(self) -> str:
        """Get arg or reply text"""
        if self.reply_to_message:
            return self.reply_to_message.text.markdown
        else:
            return self.input

    @property
    def client(self):
        return self._client

    @property
    def c(self):
        return self._client
