from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.database import Base


class Genre(Base):
    __tablename__ = 'genre'

    genre_id = Column(Integer, primary_key=True)
    name_genre = Column(String)

    books = relationship("Book", back_populates="genre")

    def __repr__(self):
        return f'Жанр [ID: {self.genre_id}, Название: {self.name_genre}]'
