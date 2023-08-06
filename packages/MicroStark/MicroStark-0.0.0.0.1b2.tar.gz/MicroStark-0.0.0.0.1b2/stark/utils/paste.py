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

from stark.utils.requests import request


async def paste(text: str, bin: str = "haste"):
    if bin.endswith("bin"):
        bin = bin[:-3]
    if bin == "space":
        base = "https://spaceb.in/"
        path = "api/v1/documents"
        res = await request(base+path, data={"content": text, "extension": "txt"})
        link = base+res["payload"]["id"]
    elif bin == "neko":
        base = "https://nekobin.com/"
        path = "api/documents"
        res = await request(base+path, json={"content": text})
        link = base+res["result"]["key"]
    elif bin == "bat":
        base = "https://batbin.me/"
        path = "api/v2/paste"
        res = await request(base+path, data=text)
        if res["success"]:
            link = base+res["message"]
        else:
            link = res["message"]
    else:
        # if not bin == "haste":
        #     logger.log(f"'{bin}' not found. Using 'haste'")
        base = "https://hastebin.com/"
        path = "documents"
        res = await request(base+path, data=text)
        link = base+res["key"]
    return link
