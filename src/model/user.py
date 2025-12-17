from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from model import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    cep = Column(String(8), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    salt = Column(String(8), nullable=False)
    password = Column(String(250), nullable=False)
    created_at = Column(String(12), nullable=False)

    symptoms = relationship("Symptom", back_populates="user")
    records = relationship("Record", back_populates="user")
    events = relationship("Event", back_populates="user")

    def __init__(self, username:str, email:str, cep:str, city:str, state:str, salt:str, password:str, created_at:str):
        self.username = username
        self.email = email
        self.cep = cep
        self.city = city
        self.state = state
        self.salt = salt
        self.password = password
        self.created_at = created_at