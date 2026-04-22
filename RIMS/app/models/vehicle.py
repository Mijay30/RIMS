from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime

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