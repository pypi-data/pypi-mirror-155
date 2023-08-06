import asyncio
import re
import json

import tgrambot
from typing import Callable

from .handler import Handler


class MessageHandler(Handler):
    def __init__(self, callback: Callable, filters=None):
        super(MessageHandler, self).__init__(callback, filters)
        self.exclude = ['callback_data']
        self.special_types = ['command', 'all', 'regex', 'text']

    async def check(self, bot: 'tgrambot.Bot', update):
        if self.filters:
            filter_type = self.filters.get('type')
            update_json = json.loads(update.message.json())
            if filter_type and update.message:
                if filter_type not in self.special_types and filter_type not in self.exclude:
                    if update_json.get(filter_type):
                        await self.callback[0](bot, update.message)
                        return True
                    else:
                        return False
                elif filter_type in self.special_types:
                    content = None
                    if filter_type == "command":
                        prefixes = self.filters.get('prefix')
                        commands = self.filters.get('command')
                        if update.message.text:
                            if type(prefixes) is str:
                                if update.message.text.startswith(prefixes):
                                    pass
                                else:
                                    return False
                            else:
                                for pre in prefixes:
                                    if update.message.text.startswith(pre):
                                        pass
                                    else:
                                        return False

                            if type(commands) is str:
                                m = re.search(commands, update.message.text, re.I)
                                if m:
                                    await self.callback[0](bot, update.message)
                                    return True
                                else:
                                    return False
                            else:
                                for command in commands:
                                    m = re.search(command, update.message.text, re.I)
                                    if m:
                                        await self.callback[0](bot, update.message)
                                        return True
                                    else:
                                        return False
                    elif filter_type == 'regex':
                        regex = self.filters.get('regex')
                        if update.message.text:
                            m = re.search(regex, update.message.text, re.I)
                            if m:
                                await self.callback[0](bot, update.message)
                                return True
                            else:
                                return False
                    elif filter_type == 'text':
                        text = self.filters.get('text')
                        if update.message.text:
                            if text:
                                m = re.search(text, update.message.text, re.I)
                                if m:
                                    await self.callback[0](bot, update.message)
                                    return True
                                else:
                                    return False
                            else:
                                await self.callback[0](bot, update.message)
                                return True
                else:
                    if update.message:
                        await self.callback[0](bot, update.message)
                        return True
                    else:
                        return False
        else:
            if update.message:
                await self.callback[0](bot, update.message)
                return True
            else:
                return False
