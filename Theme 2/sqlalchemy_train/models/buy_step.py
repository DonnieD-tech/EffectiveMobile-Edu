from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from models.database import Base


class Buy_Step(Base):
    __tablename__ = 'buy_step'

    buy_step_id = Column(Integer, primary_key=True)
    buy_id = Column(Integer, ForeignKey('buy.buy_id'))
    step_id = Column(Integer, ForeignKey('step.step_id'))
    date_step_beg = Column(Date)
    date_step_end = Column(Date)

    buy = relationship("Buy", back_populates="buy_steps")
    step = relationship("Step", back_populates="buy_steps")

    def __repr__(self):
        return f'Время обработки [ID: {self.buy_step_id}, id покупки: {self.buy_id}, Дата начала: {self.date_step_beg}, Дата начала: {self.date_step_end}]'
