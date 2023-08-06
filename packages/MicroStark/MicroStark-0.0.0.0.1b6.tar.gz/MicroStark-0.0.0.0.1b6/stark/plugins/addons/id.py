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

from stark import Stark


@Stark.cmd('id', description="Get your Telegram ID")
async def id_func(msg):
    if msg.chat.type == 'private':
        await msg.tell("Your ID is `{}`".format(msg.from_user.id))
    else:
        if msg.reply_to_message:
            await msg.tell("{}'s ID is `{}`".format(msg.reply_to_message.from_user.first_name, msg.reply_to_message.from_user.id))
        else:
            await msg.tell("Chat ID is `{}` \n\nYour ID is `{}`".format(msg.chat.id, msg.from_user.id))
