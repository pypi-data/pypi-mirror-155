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

# from pyrogram.types import Message
# from pystark import Stark, filters
# from pystark.plugins.utils import db
#
#
# @Stark.cmd(filters=~filters.service, group=2)
# async def users_sql(msg: Message):
#     if msg.from_user:
#         q = await db.get("users", msg.from_user.id)
#         if not q:
#             await db.set("users", msg.from_user.id)
#
#
# @Stark.cmd('stats', owner_only=True)
# async def stats(msg: Message):
#     users = await db.count("users")
#     await msg.reply(f"Total Users : {users}", quote=True)
