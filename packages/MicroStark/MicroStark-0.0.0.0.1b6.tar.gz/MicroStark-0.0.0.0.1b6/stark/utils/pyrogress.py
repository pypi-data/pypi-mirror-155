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

import asyncio
import humanize
from pyrogram.errors import FloodWait, MessageNotModified


async def pyrogress(current, total, message, process):
    new_current = humanize.naturalsize(current, binary=True)
    new_total = humanize.naturalsize(total, binary=True)
    # if int(float(new_current.split()[0])) % 10 != 0:
    #     return
    try:
        percentage = round((current * 100) / total, 2)
        try:
            await message.edit(f"**{process}** \n\n**Progress :** {new_current}/{new_total} | {percentage}℅")
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except MessageNotModified:  # Sometimes pyrogram returns same i think
            pass
    except ZeroDivisionError:
        try:
            await message.edit(f"**{process}** \n\n**Progress :** {new_current}")
        except FloodWait as e:
            await asyncio.sleep(e.value)
