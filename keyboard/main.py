from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class PagerAction(Enum):
    RIGHT = "right"
    LEFT = "left"


class PagerCallback(CallbackData, prefix="pager"):
    action: PagerAction
    handler: str
    page: int


def get_pager(page: int, size: int, buttons: list[InlineKeyboardButton], handler: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    buttons_ = buttons[size * 4 * page:size * 4 * (page + 1)]
    builder.add(*buttons_)
    builder.adjust(size)

    page += 1
    page_buttons = []
    if page > 1:
        page_buttons.append(InlineKeyboardButton(text=f"{page - 1} ←",
                                                 callback_data=PagerCallback(action=PagerAction.LEFT,
                                                                             handler=handler,
                                                                             page=page - 1).pack()))

    if size * 4 * page < len(buttons):
        page_buttons.append(InlineKeyboardButton(text=f"→ {page + 1}",
                                                 callback_data=PagerCallback(action=PagerAction.RIGHT,
                                                                             handler=handler,
                                                                             page=page + 1).pack()))

    builder.row(*page_buttons, width=2)

    return builder.as_markup()
