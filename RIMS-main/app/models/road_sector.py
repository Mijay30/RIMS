from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime

class PavementType(str, Enum):
    ASPHALT = "Asphalt"
    CONCRETE = "Concrete"
    GRAVEL = "Gravel"
    SOIL = "Soil"

class SectorStatus(str, Enum):
    FUNCTIONAL = "Functional"
    UNDER_MAINTENANCE = "Under Maintenance"
    CRITICAL = "Critical"
    CLOSED = "Closed"

class RoadSector(BaseModel):
    sectorId: str = Field(..., min_length=3)
    length: float
    width: float
    pavementType: PavementType
    hasDrainage: bool = True
    hasSafetyBarriers: bool = True
    status: SectorStatus = SectorStatus.FUNCTIONAL
    coordinates: List[float]
    lastModifiedBy: str
    updatedAt: datetime = Field(default_factory=datetime.now)