from sqlalchemy import Column, Integer, String
from ..database.connection import Base
from pydantic import BaseModel

class TeamMemberSQL(Base):
    __tablename__ = "team_members"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    certification_level = Column(String)
    availability_status = Column(String)
    department = Column(String)

class TeamMemberCreate(BaseModel):
    full_name: str
    certification_level: str
    availability_status: str
    department: str

class TeamMemberUpdate(BaseModel):
    availability_status: str
