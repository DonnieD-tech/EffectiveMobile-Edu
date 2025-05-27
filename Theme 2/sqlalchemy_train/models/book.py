from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.database import Base


class Book(Base):
    __tablename__ = 'book'

    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('author.author_id'))
    genre_id = Column(Integer, ForeignKey('genre.genre_id'))
    price = Column(Integer)
    amount = Column(Integer)

    author = relationship('Author', back_populates='books')
    buy_books = relationship("BuyBook", back_populates="book")
    genre = relationship('Genre', back_populates='books')

    def __repr__(self):
        return f'Книга [ID: {self.book_id}, Название: {self.title}, Автор: {self.author.name_author}, Жанр: {self.genre.name_genre}, Цена: {self.price}, Количество: {self.amount}]'
