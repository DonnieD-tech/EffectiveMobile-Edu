from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.database import Base


class Buy(Base):
    __tablename__ = 'buy'

    buy_id = Column(Integer, primary_key=True)
    buy_description = Column(String)
    client_id = Column(Integer, ForeignKey('client.client_id'))

    client = relationship("Client", back_populates="buys")
    buy_book = relationship("Buy_Book", back_populates="buy")
    buy_steps = relationship("Buy_Step", back_populates="buy")

    def __repr__(self):
        return f'Пожелание покупателя [ID: {self.buy_id}, Описание: {self.buy_description}, ID клиента: {self.client_id}, Имя клиента: {self.client.name_client}]'
