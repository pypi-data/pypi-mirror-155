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
import struct
import uvloop
import asyncio
import inspect
import logging
import importlib.util
from .logger import logger
from .types import settings
from .decorators import Mechanism
from pyrogram import Client, idle
from .constants import __version__
from stark.settings import settings
from .decorators.command import command_data
from .env import API_ID, API_HASH, BOT_TOKEN, SESSION
from pyrogram.errors import ApiIdInvalid, AccessTokenInvalid, AuthKeyUnregistered, AuthKeyDuplicated, UserDeactivated

__data__ = {"total_plugins": 0, "all_plugins": {}}


class Stark(Client, Mechanism):
    id: int
    username: str

    def __init__(
        self,
        session: str = SESSION,
        *,
        api_id: int = API_ID,
        api_hash: str = API_HASH,
        bot_token: str = BOT_TOKEN,
        in_memory: bool = True,
        name: str = 'Stark',
        **kwargs
    ):
        if not API_ID and not API_HASH and not BOT_TOKEN and not SESSION:
            logger.critical("No variables have been provided. You must provide a Bot SESSION String or API_ID, API_HASH and BOT_TOKEN")
            raise SystemExit
        if not SESSION:
            if not API_ID:
                logger.critical("Please provide SESSION (with api keys) or API_ID")
                raise SystemExit
            if not API_HASH:
                logger.critical("Please provide SESSION (with api keys) or API_HASH")
                raise SystemExit
            if not BOT_TOKEN:
                logger.critical("Please provide SESSION or BOT_TOKEN")
                raise SystemExit
        uvloop.install()
        super().__init__(
            name=name,
            session_string=session,
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token,
            in_memory=in_memory,
            app_version=f"Stark {__version__}",
            **kwargs
        )

    def activate(self=None, *, callback=None, call_with_bot: bool = False):
        client = self
        if not client:
            client = Stark()
        asyncio.get_event_loop().run_until_complete(client.main(callback, call_with_bot))

    async def main(self, callback=None, call_with_bot=False):
        logger.info("Initiated Client")
        logger.info("Starting the Bot...")
        await self.start()
        logger.info("Loading Modules...")
        await self.load_modules(settings.PLUGINS)
        await self.load_addons()
        await self._set_info()
        if callback:
            if call_with_bot:
                callback(self)
            else:
                callback()
        logger.info(f"@{self.username} is now running")
        await idle()

    async def start(self):
        try:
            return await super().start()
        except ApiIdInvalid:
            logger.critical("API_ID and API_HASH combination is incorrect.")
        except AccessTokenInvalid:
            logger.critical("BOT_TOKEN is invalid.")
        except (AuthKeyUnregistered, AuthKeyDuplicated, struct.error):
            logger.critical("Your STRING_SESSION is invalid. Please terminate it and generate a new one.")
        except UserDeactivated:
            logger.critical(f"Bot Account deleted. Time for me to rest.")
        except KeyboardInterrupt:
            logger.critical("Keyboard Interrupt. Exiting..")
        logger.info("For support visit @StarkBotsChat")
        raise SystemExit

    async def load_modules(self, plugins: str = None, addons=False):
        if addons:
            modules = await self.list_modules(addons=True)
        # elif os.path.isfile(plugins) and plugins.endswith(".py"):
        #     path, module = plugins.rsplit("/", 1)
        #     modules = [module[:-3]]
        else:
            # path = plugins
            modules = await self.list_modules(plugins)
            if not modules:
                return
        for module in modules:
            if module.endswith(".py"):
                module = module[:-3]
            # mod = importlib.import_module(path.replace("/", ".") + "." + module)
            mod = importlib.import_module(module)
            funcs = [func for func, _ in inspect.getmembers(mod, inspect.isfunction)]
            for func in funcs:
                try:
                    for handler, group in getattr(mod, func).handlers:
                        self.add_handler(handler, group)
                except AttributeError:
                    pass
            mod_name = mod.__name__
            mod_path = mod.__file__
            __data__["total_plugins"] += 1
            __data__["all_plugins"][mod_name] = mod_path
            if addons:
                logger.info("Loaded addon - {}".format(mod_name.replace('stark.plugins.addons.', '')))
            else:
                logger.info("Loaded plugin - {}".format(mod_name.replace(f"{plugins}.", "")))

    @staticmethod
    async def list_modules(directory: str = None, addons=False) -> list[str] | None:
        if addons:
            from stark.plugins import addons
            directory = getattr(addons.__path__, "_path")[0]
        if not os.path.exists(directory):
            logger.info(f"No directory named '{directory}' found")
            return
        plugs = []
        for path, _, files in os.walk(directory):
            for name in files:
                if name.endswith(".py"):
                    if addons:
                        path = 'stark.plugins.addons'
                    plugs.append(path.replace('/', '.') + '.' + name[:-3])
        return plugs

    async def load_addons(self):
        await self.load_modules(addons=True)

    @staticmethod
    def log(message: str, level=logging.INFO):
        logger.log(message, level=level)

    @property
    def data(self) -> dict:
        __data__.update(command_data)
        return __data__

    @property
    def total_plugins(self) -> int:
        return self.data["total_plugins"]

    @property
    def all_plugins(self) -> dict:
        return self.data["all_plugins"]

    @property
    def total_commands(self) -> int:
        return self.data["total_commands"]

    @property
    def all_commands(self) -> dict:
        return self.data["all_commands"]

    @property
    def sudo_commands(self) -> list[str]:
        """List of all sudo commands available. Includes `owner_only` commands too."""
        return self.data["sudo_commands"]

    # def remove_bot_menu(self):
    #     self.set_bot_commands([])
    #
    # def update_bot_menu(self):
    #     dictionary = self.data["all_commands"]
    #     commands = []
    #     for key in dictionary:
    #         if dictionary[key]:
    #             commands.append(BotCommand(key, str(dictionary[key])).write())
    #     self.send(
    #         raw.functions.bots.SetBotCommands(
    #             scope=raw.types.BotCommandScopeDefault(),
    #             lang_code='en',
    #             commands=commands
    #         )
    #     )
    #
    # async def log_tg(self, text):
    #     await self.send_message(ENV().LOG_CHAT, text)
    #     # No exceptions are handled for now.

    async def _set_info(self):
        bot = await self.get_me()
        self.id = bot.id
        self.username = bot.username
