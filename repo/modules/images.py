import logging
import typing

from sqlalchemy import Column, Integer, LargeBinary, ForeignKey

from repo.modules.base import Base, BaseRepo


class ImageData(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(LargeBinary, nullable=False)

    message_id = Column(Integer, ForeignKey('messages.id'))


class ImageRepo(BaseRepo):
    def get(self, image_id: int) -> typing.Optional[ImageData]:
        return self.session.query(ImageData).get({"id": image_id})

    def add(self, image: ImageData) -> bool:
        try:
            self.session.add(image)
            self.session.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False