import asyncio
import logging

import ollama
from aiogram import Dispatcher, Bot, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware
from sqlalchemy.util import await_only

import handlers
from keyboard.user.main import start_menu
from middlewares.users_middleware import UsersMiddleware
from utils import config
from utils.chat import Chat, in_chat
from utils.utils import check_default_admin, check_default_model

logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s][%(levelname)s][%(funcName)s][%(module)s][%(lineno)d] - %(message)s")

dp = Dispatcher()
i18n = I18n(path="locales", default_locale="en", domain="messages")

# TODO: Change to custom
dp.update.middleware(SimpleI18nMiddleware(i18n=i18n))
dp.update.middleware(UsersMiddleware())

dp.include_routers(*handlers.__all__)

ollama_client = ollama.AsyncClient(
    host=config.OLLAMA.url
)
dp["ollama_client"] = ollama_client


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext, bot: Bot):
    # await bot.unpin_all_chat_messages(chat_id=message.chat.id)

    if in_chat(await state.get_state()):
        chat: Chat = await state.get_value("chat")
        chat.exit()

    await message.answer(
        text="Hello",
        reply_markup=start_menu()
    )

    await state.clear()


@dp.callback_query(F.data == "start_menu")
async def callback_start_menu(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.delete()
    await start(message=call.message, state=state, bot=bot)


# @dp.callback_query()
# async def unhandled_callback_query(call: CallbackQuery, state: FSMContext):
#     print(call.data)


@dp.startup()
async def on_start(bot: Bot) -> None:
    await check_default_admin(bot)

    await check_default_model(ollama_client)


async def main() -> None:
    bot = Bot(
        token=config.APP.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True
        ),
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
