import asyncio
import json
from typing import Any, Coroutine

import ollama
from aiogram.fsm.context import FSMContext
from ollama import ChatResponse
from pydantic import BaseModel

from repo import repo
from repo.modules.chats import ChatData
from repo.modules.messages import MessageType, MessageData

try:
    with open("options.json") as f:
        OPTIONS = json.load(f)
except:
    OPTIONS = {}


def in_chat(state_str: str) -> bool:
    if state_str is None: return False
    return "ChatState" in state_str


class Chat:
    id: int
    ollama_client: ollama.AsyncClient

    def __init__(self, id: int, ollama_client: ollama.AsyncClient):
        self.id = id
        self.ollama_client = ollama_client

    def get_data(self) -> ChatData:
        return repo.chats.get(self.id)

    def add_message(self, message: MessageData) -> None:
        d = self.get_data()
        d.messages.append(message)
        repo.save()

    def send_message(self, message: ollama.Message, stream: bool = True):
        chat_data = self.get_data()
        messages = [ollama.Message(role=m.type.value, content=m.content) for m in chat_data.messages]
        messages.append(message)

        return self.ollama_client.chat(
            model=chat_data.model_name,
            messages=messages,
            stream=stream,
            options=OPTIONS,
        )

    async def generate_chat_title(self) -> None:
        chat_data = self.get_data()
        if chat_data.title is not None: return

        response = await self.send_message(
            message=ollama.Message(role=MessageType.USER.value,
                                   content="Write for me title that will shortly describe the main context of our dialog. GIVE ME ONLY TITLE, DO NOT WRITE IN YOUR RESPONSE ANYTHING ELSE. DO NOT EXIT LIMIT OF 50 SYMBOLS!"),
            stream=False)

        chat_data.title = response.message.content[:50]
        repo.save()

    def exit(self):
        asyncio.create_task(self.generate_chat_title())

