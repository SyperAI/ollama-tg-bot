import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from repo import repo
from repo.modules.users import UserData


class UsersMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        user: User | None = data.get("event_from_user", None)

        if user is not None:
            if repo.users.get(user.id) is None:
                if not repo.users.add(
                        UserData(
                            id=user.id,
                            language=user.language_code,
                        )
                ): logging.warning(f"User {user.id} was not added to db!")

        return await handler(event, data)
