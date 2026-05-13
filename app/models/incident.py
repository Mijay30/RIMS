from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from ..database.connection import Base

class IncidentType(str, Enum):
    POTHOLE = "Pothole"
    FALLEN_TREE = "Fallen Tree"
    DAMAGED_SIGN = "Damaged Sign"

class IncidentStatus(str, Enum):
    REPORTED = "Reported"
    ASSIGNED = "Assigned"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

class Coordinates(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class IncidentSQL(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    hazard_type = Column(String)
    description = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    status = Column(String, default="Pending")
    assigned_vehicle_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

class Incident(BaseModel):
    hazard_type: IncidentType
    description: str
    latitude: float
    longitude: float

class IncidentReport(BaseModel):
    incidentType: IncidentType
    description: str
    location: Coordinates
    status: IncidentStatus = IncidentStatus.REPORTED
    reporterId: str
    assignedVehicleId: Optional[str] = None
    lastModifiedBy: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)
