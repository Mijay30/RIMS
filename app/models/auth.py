from sqlalchemy import Column, Integer, String
from ..database.connection import Base

class UserSQL(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False) # User, Staff, Admin
    email = Column(String, unique=True, index=True, nullable=False)
