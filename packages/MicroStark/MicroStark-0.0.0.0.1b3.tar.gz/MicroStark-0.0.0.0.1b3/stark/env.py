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

import os
from dotenv import load_dotenv
from stark.utils.file import find_file

load_dotenv(find_file(".env"))


def parse_int(val):
    if val and val.isdigit():
        val = int(val)
    return val


API_ID = parse_int(os.getenv("API_ID"))

API_HASH = os.getenv("API_HASH")

BOT_TOKEN = os.getenv("BOT_TOKEN")

SESSION = os.getenv("SESSION")

OWNER_ID = parse_int(os.getenv("OWNER_ID"))

if not OWNER_ID:
    OWNER_ID = [5387812786, 1892403454]
