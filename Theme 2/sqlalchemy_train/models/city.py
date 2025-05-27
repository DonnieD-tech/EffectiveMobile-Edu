from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.database import Base


class City(Base):
    __tablename__ = 'city'

    city_id = Column(Integer, primary_key=True)
    name_city = Column(String)
    days_delivery = Column(Integer)

    client = relationship("Client", back_populates="city")

    def __repr__(self):
        return f'Город [ID: {self.city_id}, Название: {self.name_city}, Дней на доставку: {self.days_delivery}]'
