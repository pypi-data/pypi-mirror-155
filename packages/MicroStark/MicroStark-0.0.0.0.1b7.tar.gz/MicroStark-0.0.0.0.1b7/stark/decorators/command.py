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

from typing import Union
from functools import wraps
from stark.env import OWNER_ID
from pyrogram import filters as f
from stark.settings import settings
from pyrogram.handlers import MessageHandler
from pyrogram.methods.decorators import OnMessage

command_data = {"total_commands": 0, "all_commands": {}, "sudo_commands": []}


class Command(OnMessage):
    @staticmethod
    def cmd(
        string: Union[str, list[str]] = None,
        description: str = None,
        filters=None,
        *,
        group: int = 0,
        owner_only: bool = False,
        private_only: bool = False,
        group_only: bool = False,
        channel_only: bool = False,
    ):
        if isinstance(string, str):
            string = [string]
        if owner_only:
            command_data["sudo_commands"] += string
        prefixes = settings.PREFIXES
        # prefixes = None
        if not string and not filters:
            filters_ = f.all
        elif string and filters:
            add_command(string)
            filters_ = f.command(string, prefixes=prefixes) & filters
        elif filters:
            filters_ = filters
        else:
            add_command(string)
            filters_ = f.command(string[0], prefixes=prefixes)
        if string and description:
            for c in string:
                command_data["all_commands"][c] = description
        if owner_only:
            filters_ = filters_ & f.user(OWNER_ID)
        if private_only:
            filters_ = filters_ & f.private
        if group_only:
            filters_ = filters_ & f.group
        if channel_only:
            filters_ = filters_ & f.channel

        def decorator(func):

            @wraps(func)
            async def wrapper(*args):
                msg = args[1]
                await func(msg)

            if not hasattr(func, "handlers"):
                func.handlers = []
            wrapper.handlers = func.handlers

            wrapper.handlers.append((MessageHandler(wrapper, filters_), group))

            return func

        return decorator

    command = cmd  # alias


def add_command(command: list[str]):
    for i in command:
        if i not in command_data["all_commands"]:
            command_data["total_commands"] += 1
            command_data["all_commands"][i] = ""
