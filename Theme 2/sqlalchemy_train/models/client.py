from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.database import Base


class Client(Base):
    __tablename__ = 'client'

    client_id = Column(Integer, primary_key=True)
    name_client = Column(String)
    city_id = Column(Integer, ForeignKey('city.city_id'))
    email = Column(String)

    city = relationship("City", back_populates="clients")
    buys = relationship("Buy", back_populates="client")


    def __repr__(self):
        return f'Клиент [ID: {self.client_id}, Имя: {self.name_client}, E-mail: {self.email}, Город: {self.city.name_city}]'
