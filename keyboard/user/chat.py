from typing import List

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboard.main import get_pager
from repo.modules.chats import ChatData


class ChatCallback(CallbackData, prefix="join_chat"):
    id: int


def chat_menu(current_model: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text=current_model, callback_data="change_chat_model"))

    return builder.as_markup()


def chat_list_kb(chats: List[ChatData], page: int = 0) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text=chat.title if chat.title is not None else "New Chat",
            callback_data=ChatCallback(id=chat.id).pack()
        ) for chat in chats
    ]

    builder = InlineKeyboardBuilder.from_markup(get_pager(buttons=buttons, page=page, size=2, handler="chat"))

    builder.row(
        InlineKeyboardButton(text=_("← Back"), callback_data="start_menu")
    )

    return builder.as_markup()
