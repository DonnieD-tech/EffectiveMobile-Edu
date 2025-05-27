from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.database import Base


class Step(Base):
    __tablename__ = 'step'

    step_id = Column(Integer, primary_key=True)
    name_step = Column(String)

    buy_steps = relationship("Buy_Step", back_populates="step")

    def __repr__(self):
        return f'Статус [ID: {self.step_id}, Название: {self.name_step}]'
