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

import functools
from pyrogram.errors import PeerIdInvalid, UsernameInvalid


class Extras:
    @staticmethod
    def ref_required(func):
        """User ID or Reply to User required."""
        @functools.wraps(func)
        async def wrapper(msg):
            try:
                if not msg.reply_to_message and not msg.args:
                    await msg.tell("REF_REQUIRED")
                    return
                await func(msg)
            except UsernameInvalid:
                await msg.tell("USERNAME_INVALID")
            except PeerIdInvalid:
                await msg.tell("PEER_ID_INVALID")

        wrapper.__filepath__ = func.__code__.co_filename
        return wrapper

    @staticmethod
    def arg_required(what: str):
        """Argument required"""
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(msg):
                if not msg.args:
                    await msg.tell("ARG_REQUIRED", format=what)
                    return
                await func(msg)

            wrapper.__filepath__ = func.__code__.co_filename
            return wrapper

        return decorator

    @staticmethod
    def reply_required(func):
        """Reply to a message required"""
        @functools.wraps(func)
        async def wrapper(msg):
            if not msg.reply_to_message:
                await msg.tell("REPLY_REQUIRED")
                return
            await func(msg)

        wrapper.__filepath__ = func.__code__.co_filename
        return wrapper

    @staticmethod
    def aor_required(func):
        """Arg or Reply: Reply to a message or passing an argument required"""
        @functools.wraps(func)
        async def wrapper(msg):
            if not msg.reply_to_message and not msg.args:
                await msg.tell("AOR_REQUIRED")
                return
            await func(msg)

        wrapper.__filepath__ = func.__code__.co_filename
        return wrapper
