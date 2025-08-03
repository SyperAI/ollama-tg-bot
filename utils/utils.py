import logging
import sys

import ollama
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from ollama import ResponseError, AsyncClient

from repo import repo
from repo.modules.chats import ChatData
from repo.modules.messages import MessageType
from repo.modules.users import UserRole
from utils import config


async def check_default_admin(bot: Bot) -> None:
    admin_user = repo.users.get(config.APP.admin_id)

    if admin_user is None:
        logging.warning(
            f"Default admin user not found.Run the bot from the account with id={config.APP.admin_id} and restart the bot!")
        return

    if admin_user.role != UserRole.ADMIN:
        admin_user.role = UserRole.ADMIN
        repo.save()

        await bot.send_message(
            chat_id=admin_user.id,
            text="You were issued administrator rights"
        )


async def check_default_model(ollama: AsyncClient) -> None:
    models_list = await ollama.list()
    model_exists = False

    for model in models_list.models:
        if config.OLLAMA.default_model in model.model:
            model_exists = True

    if not model_exists:
        logging.info("Default model not found. Trying to download it...")
        try:
            await ollama.pull(config.OLLAMA.default_model)
        except ResponseError as e:
            logging.critical(f"Some error occurred while trying to download default model: {e}")
            return sys.exit(1)

    logging.info(f"Default ollama model {config.OLLAMA.default_model} found")



