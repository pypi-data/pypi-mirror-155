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

from stark.logger import logger


def patch(obj):
    try:
        patch_list = getattr(obj, "__patch__")
        if not isinstance(patch_list, list):
            logger.warn("__patch__ attribute must be a list. Skipping patch..")
            return
    except AttributeError:
        patch_list = []
    try:
        no_patch_list = getattr(obj, "__no_patch__")
        if not isinstance(no_patch_list, list):
            logger.warn("__no_patch__ attribute must be a list. Skipping patch..")
            return
    except AttributeError:
        no_patch_list = []

    def is_patchable(name):
        if name in no_patch_list:
            return False
        elif patch_list and name not in patch_list:
            return False
        return True

    def wrapper(container):
        attrs = vars(container)
        for name in attrs:
            attr = attrs[name]
            if name.startswith("__") and name.endswith("__"):
                continue
            if is_patchable(name):
                old = getattr(obj, name, None)
                setattr(obj, 'old_' + name, old)
                setattr(obj, name, attr)
        return container

    return wrapper
