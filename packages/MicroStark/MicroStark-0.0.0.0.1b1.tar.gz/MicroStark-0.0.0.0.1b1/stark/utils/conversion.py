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

# import os
# from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
#
# sep = "$buttons$"
#
#
# async def extract_msg_data(string: str):
#     if sep in string.lower():
#         x = string.lower()
#         s = x.find(sep)
#         e = x.find(sep)+len(sep)
#         text = string[:s].strip()
#         buttons = string[e:].strip()
#     else:
#         text = string
#         buttons = None
#     buttons = await string_to_buttons(buttons)
#     return text, buttons
#
#
# async def string_to_buttons(string) -> None | InlineKeyboardMarkup:
#     if not string:
#         return
#     buttons = []
#     rows = string.split('\n')
#     for row in rows:
#         row_buttons = []
#         r_b = row.split("|")
#         for b in r_b:
#             data = b.split('-', 1)
#             if len(data) < 2:
#                 continue
#             text = data[0].strip()
#             but = data[1].strip()
#             data = but.split(":", 1)
#             if len(data) < 2:
#                 continue
#             button_type = data[0].strip()
#             ans = data[1].strip()
#             if button_type == "alert":
#                 row_buttons.append(InlineKeyboardButton(text, callback_data=f"alert+{ans}"))
#             else:
#                 row_buttons.append(InlineKeyboardButton(text, url=ans))
#         buttons.append(row_buttons)
#     if buttons:
#         buttons = InlineKeyboardMarkup(buttons)
#     return buttons
#
#
# def get_db_url(i: str):
#     i = os.environ.get(i, "").strip()
#     if 'postgres' in i and 'postgresql' not in i:
#         i = i.replace("postgres", "postgresql")
#     if "psycopg2" not in i:
#         i = i.replace("postgresql", "postgresql+psycopg2")
#     return i
#
#
# async def list_to_string(data: list, pref: str = None) -> str:
#     string = ""
#     num = 0
#     for i in data:
#         num += 1
#         if not pref:
#             if isinstance(i, int) or (isinstance(i, str) and i.isdigit()):
#                 i = f"`{i}`"
#             string += f"{num}) {i}\n"
#         else:
#             text = f"{pref}{i}"
#             if pref != "/":
#                 text += f"`{text}`"
#             string += text
#     return string
