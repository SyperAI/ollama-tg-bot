import datetime
import enum
import logging
import typing

from sqlalchemy import Column, Integer, ForeignKey, Enum, Text, DateTime
from sqlalchemy.orm import relationship

from repo.modules.base import Base, BaseRepo


class MessageType(enum.Enum):
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'


class MessageData(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum(MessageType), nullable=False)
    sent_at = Column(DateTime, default=datetime.datetime.now)

    content = Column(Text, nullable=False)
    images = relationship('ImageData')

    chat_id = Column(Integer, ForeignKey('chats.id'))
    chat = relationship('ChatData', backref='messages')

    def __str__(self):
        # Если ImageData у вас тоже переопределяет __str__, можно просто: imgs = [str(img) for img in self.images]
        imgs = [f"{img.id}" for img in self.images]
        return (
            f"<MessageData id={self.id!r} "
            f"type={self.type.name!r} "
            f"chat_id={self.chat_id!r} "
            f"content={self.content!r} "
            f"images={imgs}>"
        )


class MessageRepo(BaseRepo):
    def get(self, message_id: int) -> typing.Optional[MessageData]:
        return self.session.query(MessageData).get({"id": message_id})

    def add(self, message: MessageData) -> bool:
        try:
            self.session.add(message)
            self.session.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False
