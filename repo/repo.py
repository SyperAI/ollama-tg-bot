from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from repo.modules.base import Base
from repo.modules.chats import ChatRepo
from repo.modules.images import ImageRepo
from repo.modules.messages import MessageRepo
from repo.modules.users import UsersRepo


class Repo:
    def __init__(self, username: str, password: str, host: str, port: int, db: str) -> None:
        with create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}").connect() as conn:
            conn.execute(
                text(f"CREATE DATABASE IF NOT EXISTS `{db}` "
                     f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            )
            conn.commit()

        self.engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{db}')

        self._Session = sessionmaker(bind=self.engine)
        self.session = self._Session()

        Base.metadata.create_all(self.engine)

    def save(self) -> None:
        self.session.commit()

    @property
    def users(self) -> UsersRepo:
        return UsersRepo(session=self.session)

    @property
    def chats(self) -> ChatRepo:
        return ChatRepo(session=self.session)

    @property
    def messages(self) -> MessageRepo:
        return MessageRepo(session=self.session)

    @property
    def images(self) -> ImageRepo:
        return ImageRepo(session=self.session)