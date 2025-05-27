from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.database import Base


class Author(Base):
    __tablename__ = 'author'

    author_id = Column(Integer, primary_key=True)
    name_author = Column(String)

    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return f'Автор [ID: {self.author_id}, Имя: {self.name_author}]'
