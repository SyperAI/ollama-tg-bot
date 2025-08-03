import datetime
import logging

import ollama
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from repo.modules.base import Base, BaseRepo



class ChatData(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    created_at = Column(DateTime, default=datetime.datetime.now)

    owner_id = Column(BigInteger, ForeignKey('users.id'))
    owner = relationship('UserData', backref='chats')

    model_name = Column(String(50))

    system_prompt = Column(Text, default='')


    def send_message(self, ollama_client: ollama.AsyncClient, message: ollama.Message, stream: bool = True):
        messages = [ollama.Message(role=m.type.value, content=m.content) for m in self.messages]
        messages.append(message)

        return ollama_client.chat(
            model=self.model_name,
            messages=messages,
            stream=stream
        )




class ChatRepo(BaseRepo):
    def __init__(self, session):
        super().__init__(session)

    def add(self, chat: ChatData) -> bool:
        try:
            self.session.add(chat)
            self.session.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False

    def get(self, chat_id: int) -> ChatData | None:
        return self.session.query(ChatData).get({"id": chat_id})
