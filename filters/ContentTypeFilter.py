from aiogram.filters import Filter
from aiogram.types import Message


class ContentTypeFilter(Filter):
    def __init__(self, *args) -> None:
        self.type = args

    async def __call__(self, message: Message) -> bool:
        return message.content_type in self.type
