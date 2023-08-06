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

from PIL import Image


async def to_webp(path: str) -> str:
    name = path.rsplit(".", 1)[0]+".webp"
    im = Image.open(path).convert("RGB")
    width, height = im.size
    max_pixels = 512
    ratio = min(max_pixels/width, max_pixels/height)
    size = (int(ratio*width), int(ratio*height))
    im.resize(size)
    im.save(name, "webp")
    return name
