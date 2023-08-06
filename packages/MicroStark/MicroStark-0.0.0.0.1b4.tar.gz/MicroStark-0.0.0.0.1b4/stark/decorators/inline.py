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

from stark.utils.filters import get_filters
from pyrogram.methods.decorators.on_inline_query import OnInlineQuery


class Inline(OnInlineQuery):
    @staticmethod
    def inline(
        query: str | list[str] = None,
        negate: str | list[str] = None,
        startswith: bool = False,
        owner_only: bool = False,
        group: int = 0,
        filters=None,
    ):
        filters_ = get_filters("inline", query, negate, filters, startswith, owner_only)
        decorator = OnInlineQuery.on_inline_query(filters_, group)
        return decorator

    il = inline
