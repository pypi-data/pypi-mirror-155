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

import os.path
from .types.settings import Settings


def get_settings():
    from stark import default_settings
    if os.path.exists("settings.py"):
        file = __import__("settings")
        for i in dir(default_settings):
            if i.isupper() and i not in dir(file):
                setattr(file, i, getattr(default_settings, i))
    else:
        file = default_settings
    return file


settings: Settings = get_settings()
