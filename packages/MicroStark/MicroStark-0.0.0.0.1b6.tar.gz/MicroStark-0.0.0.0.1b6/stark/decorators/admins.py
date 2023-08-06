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
from pyrogram.errors import ChatAdminInviteRequired, UserAdminInvalid


aliases = {
    'edit': 'can_be_edited',
    'manage': 'can_manage_chat',
    'delete': 'can_delete_messages',
    'restrict': 'can_restrict_members',
    'promote': 'can_promote_members',
    'change': 'can_change_info',
    'invite': 'can_invite_users',
    'pin': 'can_pin_messages',
    'vc': 'can_manage_voice_chats',
}


class Admins:
    @staticmethod
    def admins(alias: str = "", reply: bool = False):
        def first_decorator(func):
            if alias and alias in aliases:
                perm = aliases[alias]
            elif alias in list(aliases.values()):
                perm = alias
            else:
                perm = None

            @functools.wraps(func)
            async def wrapper(msg):
                bot = msg.c
                bot_status = (await msg.chat.get_member(bot.id))
                if bot_status.status != 'administrator':
                    if reply:
                        await msg.tell("I_AM_NOT_ADMIN")
                    return
                if perm and not bot_status[perm]:
                    if reply:
                        await msg.tell("I_DONT_HAVE_RIGHT", format=perm)
                    return
                try:
                    await func(msg)
                except ChatAdminInviteRequired:
                    if reply:
                        await msg.tell("USER_NOT_PRESENT")
                except UserAdminInvalid:
                    if reply:
                        await msg.tell("NOT_ENOUGH_RIGHTS")
            wrapper.__filepath__ = func.__code__.co_filename
            return wrapper

        return first_decorator
