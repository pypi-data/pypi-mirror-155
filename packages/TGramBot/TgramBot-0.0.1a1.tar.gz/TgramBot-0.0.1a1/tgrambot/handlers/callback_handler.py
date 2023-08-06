import asyncio
import re

import tgrambot
from typing import Callable

from .handler import Handler


class CallbackQueryHandler(Handler):
    def __init__(self, callback: Callable, filters=None):
        super(CallbackQueryHandler, self).__init__(callback, filters)
        self.required_filters = ['callback_data', 'regex']

    async def check(self, bot: 'tgrambot.Bot', update):
        if self.filters:
            filter_type = self.filters.get('type')
            if filter_type and filter_type in self.required_filters and update.callback_query:
                if filter_type == "callback_data":
                    if update.callback_query.data:
                        data = self.filters.get('data')
                        m = re.search(data, update.callback_query.data, re.I)
                        if m:
                            await self.callback[0](bot, update.callback_query)
                            return True
                        else:
                            return False
                    else:
                        return False
                elif filter_type == "regex":
                    regex = self.filters.get('regex')
                    if update.callback_query.data:
                        m = re.search(regex, update.callback_query.data, re.I)
                        if m:
                            await self.callback[0](bot, update.callback_query)
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
        else:
            await self.callback[0](bot, update.callback_query)
            return True
