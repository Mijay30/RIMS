from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from ..database.connection import Base

class VehicleStatus(str, Enum):
    AVAILABLE = "Available"
    MAINTENANCE = "Maintenance"
    BUSY = "Busy"

class VehicleType(str, Enum):
    ASPHALT_PAVER = "Asphalt Paver"
    SNOWPLOW = "Snowplow"
    POTHOLE_REPAIR = "Pothole Repair"
    TREE_REMOVAL = "Tree Removal"
    GENERAL = "General"

class VehicleSQL(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    registration_number = Column(String, unique=True, index=True)
    vehicle_type = Column(String)
    capacity = Column(String)
    is_available = Column(Boolean, default=True)
    status = Column(String)
    assigned_team_id = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.now)

class Vehicle(BaseModel):
    registrationNumber: str = Field(..., min_length=5)
    vehicleType: VehicleType
    capacity: str
    equipment: List[str]
    isAvailable: bool = True
    status: VehicleStatus = VehicleStatus.AVAILABLE
    assignedTeamId: Optional[str] = None
    lastModifiedBy: str
    updatedAt: datetime = Field(default_factory=datetime.now)