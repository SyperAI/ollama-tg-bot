from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text=_("New Chat"), callback_data="new_chat"),
        InlineKeyboardButton(text=_("Chats list"), callback_data="chats_list"),
    )

    return builder.as_markup()