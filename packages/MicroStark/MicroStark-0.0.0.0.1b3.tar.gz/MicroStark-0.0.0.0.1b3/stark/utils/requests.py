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

import aiohttp
from aiohttp import ClientResponse


aio = aiohttp.ClientSession()


class Request:
    @staticmethod
    async def request(method: str, url: str, get_json: bool = True, **kwargs) -> dict[str] | ClientResponse:
        if method.lower() == "get":
            response = await aio.get(url, **kwargs)
        else:
            response = await aio.post(url, **kwargs)
        response.raise_for_status()
        if get_json:
            return await response.json()
        else:
            return response

    async def get(self, url: str, params: dict = None, get_json: bool = True, **kwargs):
        return await self.request("get", url, params=params, get_json=get_json, **kwargs)

    async def post(self, url: str, json: dict = None, data: str | dict = None, get_json: bool = True, **kwargs):
        return await self.request("post", url, json=json, data=data, get_json=get_json, **kwargs)


request = Request()
