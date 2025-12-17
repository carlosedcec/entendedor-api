from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from model import Base

class Symptom(Base):
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(100), nullable=False)
    order = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    records = relationship("Record", back_populates="symptom")
    user = relationship("User", back_populates="symptoms")

    def __init__(self, name:str, order:int, user_id: int):
        self.name = name
        self.order = order
        self.user_id = user_id