from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.database import Base


class Buy_Book(Base):
    __tablename__ = 'buy_book'

    buy_book_id = Column(Integer, primary_key=True)
    buy_id = Column(Integer, ForeignKey('buy.buy_id'))
    book_id = Column(Integer, ForeignKey('book.book_id'))
    amount = Column(Integer)

    buy = relationship("Buy", back_populates="buy_books")
    book = relationship("Book", back_populates="buy_books")

    def __repr__(self):
        return f'Заказы [ID: {self.buy_book_id}, Книги: {self.book.title}, Количество: {self.amount}]'
