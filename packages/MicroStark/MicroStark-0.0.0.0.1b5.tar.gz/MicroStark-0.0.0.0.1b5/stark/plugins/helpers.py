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
from stark.env import OWNER_ID
from stark.settings import settings
from pyrogram.errors import PeerIdInvalid
# from pystark.database.sql import Database


# module = settings
db = None


async def replace(m, msg):
    if '{user}' in m:
        m = m.replace("{user}", msg.from_user.first_name)
    if '{bot}' in m:
        m = m.replace("{bot}", (await msg.c.get_me()).first_name)
    if '{user_mention}' in m:
        m = m.replace("{user_mention}", msg.from_user.mention)
    if '{bot_mention}' in m:
        m = m.replace("{bot_mention}", (await msg.c.get_me()).mention)
    if '{owner}' in m:
        owner = '@pystark'
        if OWNER_ID:
            try:
                owner = (await msg.c.get_users(OWNER_ID[0])).mention
            except PeerIdInvalid:
                Stark.log(f"Can't interact with bot owner [user={OWNER_ID[0]}]. Please send a message to bot.", "warn")
        m = m.replace("{owner}", owner)
    return m


def send_buttons():
    if settings.BUTTONS is False:
        return False
    else:
        return True


cache_commands = ""


async def replace_commands(bot: Stark, text: str):
    global cache_commands
    if cache_commands:
        return cache_commands
    basics = {"1": "", "2": "", "3": "", "4": ""}
    others = []
    cmds = bot.all_commands
    for c in cmds:
        if cmds[c]:
            x = f"/{c} - {cmds[c]} \n"
            if c == "start":
                basics["1"] = x
            elif c == "help":
                basics["2"] = x
            elif c == "about":
                basics["3"] = x
            elif c == "id":
                basics["4"] = x
            else:
                others.append(x)
    basics_str = basics["1"] + basics["2"] + basics["3"] + basics["4"]
    others_str = "".join(others)
    text = text.replace("{commands}", others_str+basics_str)
    cache_commands = text
    return text
