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

import pytz
import logging
import datetime


class Formatter(logging.Formatter):
    """ Override logging.Formatter"""
    # Taken from https://stackoverflow.com/a/67241679

    def formatTime(self, record, datefmt):
        date = datetime.datetime.fromtimestamp(record.created, tz=pytz.UTC)
        date = date.astimezone(pytz.timezone("Asia/Kolkata"))
        return date.strftime(datefmt)


logger = logging.getLogger("stark_log")
logger.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
console.setFormatter(formatter)
logger.addHandler(console)
logger.propagate = False
