from ._base import Base
from sqlalchemy import Column, Integer, String


class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(1024), nullable=True)
    url = Column(String(1024), nullable=True)
    created = Column(String(100), nullable=True)

    def __repr__(self):
        return f'{self.id} - {self.title}'
