import enum
import logging
import typing

from sqlalchemy import Column, Integer, String, Enum, BigInteger

from repo.modules.base import Base, BaseRepo
from utils import config


class UserRole(enum.Enum):
    USER = 1
    ADMIN = 128

class UserData(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    language = Column(String(4), default='en')

    model_name = Column(String(50), default=config.OLLAMA.default_model)

    # STATS
    msg_count = Column(Integer, default=0)
    role = Column(Enum(UserRole), default=UserRole.USER)


class UsersRepo(BaseRepo):
    def __init__(self, session):
        super().__init__(session)

    def add(self, user: UserData) -> bool:
        if self.get(user.id) is not None: return False

        try:
            self.session.add(user)
            self.session.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False

    def get(self, user_id) -> typing.Optional[UserData]:
        return self.session.query(UserData).get({"id": user_id})