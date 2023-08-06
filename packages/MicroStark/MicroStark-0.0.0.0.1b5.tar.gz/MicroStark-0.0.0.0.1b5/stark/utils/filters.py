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

from stark.env import OWNER_ID
from stark.logger import logger
from pyrogram import filters as f


def get_filters(
    query_type: list[str] | str,
    query,
    negate,
    extra_filters,
    startswith: bool,
    owner_only: bool
):
    if query_type == "inline":
        string = "query"
    else:
        string = "data"
    if isinstance(query, list):
        cmd_filter = f.create(lambda _, __, query_: getattr(query_, string).lower() in query)
    elif isinstance(query, str):
        query = query.lower()
        if not startswith:
            cmd_filter = f.create(lambda _, __, query_: getattr(query_, string).lower() == query)
        else:
            cmd_filter = f.create(lambda _, __, query_: getattr(query_, string).lower().startswith(query))
    elif not query:
        cmd_filter = None
    else:
        logger.warn(f'{query_type.lower()}: query cannot be of query_type {type(query)} - {query}]')
        return
    if negate:
        negate_filter = ~f.create(lambda _, __, query_: getattr(query_, string).lower() in negate)
        if cmd_filter:
            cmd_filter = cmd_filter & negate_filter
        else:
            cmd_filter = negate_filter
    if extra_filters:
        filters_ = cmd_filter & extra_filters
    else:
        filters_ = cmd_filter
    if owner_only:
        filters_ = filters_ & f.user(OWNER_ID)
    return filters_
