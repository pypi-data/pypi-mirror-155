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

import json


class PrettyDict(dict):
    def __init__(self, data: dict = None):
        if data:
            for i in data:
                if isinstance(data[i], dict):
                    data[i] = PrettyDict(data[i])
                self[i] = data[i]
        super().__init__()

    def __str__(self):
        return json.dumps(self, indent=4, default=str)

    @property
    def self(self):
        return self
