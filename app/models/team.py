from sqlalchemy import Column, Integer, String, Boolean
from ..database.connection import Base
from pydantic import BaseModel, ConfigDict

class TeamMemberSQL(Base):
    __tablename__ = "team_members"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    certification_level = Column(String)
    availability_status = Column(String)
    is_available = Column(Boolean, default=True)
    department = Column(String)

class TeamMemberCreate(BaseModel):
    full_name: str
    certification_level: str
    availability_status: str
    is_available: bool = True
    department: str

class TeamMemberUpdate(BaseModel):
    availability_status: str
    is_available: bool = True

class TeamMember(BaseModel):
    id: int
    full_name: str
    certification_level: str
    availability_status: str
    is_available: bool
    department: str

    model_config = ConfigDict(from_attributes=True)
