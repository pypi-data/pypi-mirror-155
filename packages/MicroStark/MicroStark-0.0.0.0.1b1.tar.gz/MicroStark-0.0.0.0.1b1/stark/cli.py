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
import sys
import argparse
from .constants import __description__, __version__


def main():
    parser = argparse.ArgumentParser(
        prog='stark',
        description=__description__,
        usage='%(prog)s [options]',
        epilog='Enjoy the program :)',
        allow_abbrev=False,
        add_help=False
    )
    parser.add_argument('-v', '--version', help='check the current stark version installed', action='store_true')
    parser.add_argument('-bp', '--boilerplate', help='create boilerplate in current folder', action='store_true')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    if args.version:
        print(f'v{__version__}')
        return
    if args.boilerplate:
        cwd = os.getcwd()
        print('Generating Boilerplate...')
        print("cwd = ", cwd)
        print('Done. Boilerplate is ready!')
