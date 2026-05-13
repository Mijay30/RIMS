from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from ..database.connection import Base

class VehicleStatus(str, Enum):
    AVAILABLE = "Available"
    MAINTENANCE = "Maintenance"
    BUSY = "Busy"

class VehicleType(str, Enum):
    ASPHALT_LAYING = "Asphalt-laying machine"
    POTHOLE_REPAIR = "Pothole repair unit"
    SNOW_REMOVAL = "Snow-removal vehicle"

class VehicleTypeSQL(Base):
    __tablename__ = "vehicle_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class VehicleSQL(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    registration_number = Column(String, unique=True, index=True)
    vehicle_type = Column(String)
    capacity = Column(String)
    equipment_type = Column(String)
    availability_status = Column(String)
    maintenance_status = Column(String)
    maintenance_history = Column(String)
    is_available = Column(Boolean, default=True)
    status = Column(String)
    assigned_team_id = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    updated_at = Column(DateTime, default=datetime.now)

class Vehicle(BaseModel):
    registrationNumber: str = Field(..., min_length=5)
    vehicleType: str
    capacity: str
    equipment_type: str
    availability_status: str
    maintenanceStatus: str
    maintenance_history: str
    isAvailable: bool = True
    status: VehicleStatus = VehicleStatus.AVAILABLE
    assignedTeamId: Optional[str] = None
    lastModifiedBy: str
    updatedAt: datetime = Field(default_factory=datetime.now)