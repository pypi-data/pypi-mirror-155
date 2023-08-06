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
from stark.settings import settings
from ..constants import HOME_BUTTON, HELP
from pyrogram.types import InlineKeyboardMarkup
from ..helpers import replace, send_buttons, replace_commands

help = HELP.replace("{1}", settings.HELP)


@Stark.cmd('help', description="How to use the bot?", private_only=True)
async def help_func(msg):
    try:
        text = help
        if "{commands}" in text:
            text = await replace_commands(msg.c, text)
        text = await replace(text, msg)
        if send_buttons():
            await msg.tell(text, reply_markup=InlineKeyboardMarkup(HOME_BUTTON))
        else:
            await msg.tell(text)
    except AttributeError:
        pass
