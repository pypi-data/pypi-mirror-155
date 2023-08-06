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
from ..constants import HOME_BUTTON, ABOUT
from ..helpers import replace, send_buttons
from pyrogram.types import InlineKeyboardMarkup

about = ABOUT.replace("{1}", settings.ABOUT).replace("{2}", settings.REPO)


@Stark.cmd('about', description="About the bot", private_only=True)
async def about_func(msg):
    try:
        text = await replace(about, msg)
        if send_buttons():
            await msg.tell(text, reply_markup=InlineKeyboardMarkup(HOME_BUTTON))
        else:
            await msg.tell(text)
    except AttributeError:
        pass
