import time
from typing import List

import ollama
from aiogram import Router, F, Bot
from aiogram.enums import ChatAction, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n import gettext as _

from filters.ContentTypeFilter import ContentTypeFilter
from keyboard.main import PagerCallback
from keyboard.user.chat import chat_menu, chat_list_kb, ChatCallback
from repo import repo
from repo.modules.chats import ChatData
from repo.modules.messages import MessageData, MessageType
from states.chat import ChatState
from utils.chat import Chat

chats_router = Router()


@chats_router.callback_query(F.data == "new_chat")
async def new_chat(call: CallbackQuery, state: FSMContext, ollama_client: ollama.AsyncClient) -> None:
    text = _(
        "The chat is created, for interaction with AI, just write into the chat. Use this message to control, it will be automatically fixed.")
    user = repo.users.get(call.from_user.id)

    chat = ChatData(
        owner_id=user.id,
        model_name=user.model_name
    )
    if not repo.chats.add(chat):
        await call.answer(text=_("Something went wrong. Try again later."), show_alert=True)
        return

    await state.set_state(ChatState.WAITING_MESSAGE)
    await state.set_data({'chat': Chat(id=chat.id, ollama_client=ollama_client)})

    # TODO: Add try-catch
    await call.message.edit_text(
        text=text,
        reply_markup=chat_menu(chat.model_name)
    )
    await call.message.pin()


@chats_router.callback_query(F.data == "chats_list")
async def chats_list(call: CallbackQuery) -> None:
    chats: List[ChatData] = repo.users.get(call.from_user.id).chats

    text = _("Choose chat to join")
    await call.message.edit_text(
        text=text,
        reply_markup=chat_list_kb(chats)
    )


@chats_router.callback_query(ChatCallback.filter())
async def join_chat(call: CallbackQuery, state: FSMContext, callback_data: ChatCallback,
                    ollama_client: ollama.AsyncClient) -> None:
    chat_data = repo.chats.get(callback_data.id)
    if chat_data is None:
        await call.message.answer(text=_("Something went wrong. Try again later."), show_alert=True)
        return

    await state.set_state(ChatState.WAITING_MESSAGE)
    await state.set_data({'chat': Chat(id=chat_data.id, ollama_client=ollama_client)})

    # TODO: Add try-catch
    await call.message.edit_text(
        text=_(
            "The chat is created, for interaction with AI, just write into the chat. Use this message to control, it will be automatically fixed."),
        reply_markup=chat_menu(chat_data.model_name)
    )
    await call.message.pin()


@chats_router.callback_query(PagerCallback.filter(F.handler == "chat"))
async def pager(call: CallbackQuery, callback_data: PagerCallback) -> None:
    chats: List[ChatData] = repo.users.get(call.from_user.id).chats

    await call.message.edit_reply_markup(
        reply_markup=chat_list_kb(chats, page=callback_data.page-1)
    )


# TODO
@chats_router.callback_query(ChatState(), F.data == "change_chat_model")
async def change_chat_model(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer(text="TODO")


@chats_router.message(ChatState.WAITING_MESSAGE, ContentTypeFilter(ContentType.TEXT))
async def receive_chat_message(message: Message, state: FSMContext, bot: Bot) -> None:
    chat: Chat = await state.get_value("chat")

    # chat: ChatData = repo.chats.get(await state.get_value('chat_id'))
    chat.add_message(MessageData(type=MessageType.USER, content=message.text))

    await state.set_state(ChatState.WAITING_RESPONSE)
    response_msg = await message.reply(text=_("Generating response..."))

    last_time = time.time()
    response = ""
    response_time = 0

    # response: ChatResponse = await chat.send_message(ollama_client, ollama.Message(role=MessageType.USER.value, content=message.text))
    async for part in await chat.send_message(ollama.Message(role=MessageType.USER.value, content=message.text)):
        response += part.message.content

        c_chat = await state.get_value("chat")
        if c_chat is None or c_chat.id != chat.id:
            await response_msg.edit_text(text=response)
            return

        if not part.done:
            if time.time() - last_time > 1:
                await bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
                await response_msg.edit_text(text=response)
                last_time = time.time()
        else:
            response_time = part.total_duration / 1e9

    chat.add_message(MessageData(type=MessageType.ASSISTANT, content=response))

    await state.set_state(ChatState.WAITING_MESSAGE)

    text = _("{response}"
             "\n\n<b>Model:</b> <code>{model_name}</code>"
             "\n<i>Generated in {r_time:.2f}s</i>").format(
        response=response,
        model_name=chat.get_data().model_name,
        r_time=response_time
    )
    await response_msg.edit_text(text=text)


@chats_router.message(ChatState.WAITING_MESSAGE)
async def unsupported_chat_message(message: Message) -> None:
    await message.reply(text=_("Sorry but currently I can't work with this message type 😓"))