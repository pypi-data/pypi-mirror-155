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

from .help import help
from stark import Stark
from .start import start
from .about import about
from ..constants import HOME_BUTTON, MAIN_BUTTONS
from pyrogram.types import InlineKeyboardMarkup, CallbackQuery
from ..helpers import replace, replace_commands


@Stark.callback(query=['home', 'about', 'help'])
async def basic_cb(bot: Stark, cb: CallbackQuery):
    chat_id = cb.from_user.id
    message_id = cb.message.id
    if cb.data == 'home':
        text = await replace(start, cb.message)
        buttons = MAIN_BUTTONS
    elif cb.data == 'about':
        text = await replace(about, cb.message)
        buttons = HOME_BUTTON
    else:
        text = str(help)
        if "{commands}" in text:
            text = await replace_commands(bot, text)
        text = await replace(text, cb.message)
        buttons = HOME_BUTTON
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True,
    )
