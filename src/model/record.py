from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from model.base import Base

class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, unique=True)
    symptom_id = Column(Integer, ForeignKey("symptoms.id"), nullable=False)
    date = Column(String(9), nullable=False)
    time = Column(String(12), nullable=False)
    value = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    symptom = relationship("Symptom", back_populates="records")
    user = relationship("User", back_populates="records")

    def __init__(self, symptom_id: int, date: str, time: str, value: int, user_id: int):
        self.symptom_id = symptom_id
        self.date = date
        self.time = time
        self.value = value
        self.user_id = user_id