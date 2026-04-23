from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime

class IncidentType(str, Enum):
    POTHOLE = "Pothole"
    FALLEN_TREE = "Fallen Tree"
    DAMAGED_SIGN = "Damaged Road Sign"
    FLOODING = "Road Flooding"
    OTHER = "Other Hazard"

class IncidentStatus(str, Enum):
    REPORTED = "Reported"
    ASSIGNED = "Assigned"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

class Coordinates(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

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