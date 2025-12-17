from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from model.base import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, unique=True)
    description = Column(String(255), nullable=False)
    date = Column(String(9), nullable=False)
    time = Column(String(12), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="events")

    def __init__(self, description:str, date:str, time:str, user_id: int):
        self.description = description
        self.date = date
        self.time = time
        self.user_id = user_id