from sqlalchemy import Column, Integer, String, Float
from ..database import Base
from pydantic import BaseModel, ConfigDict

class RoadSegmentSQL(Base):
    __tablename__ = "road_segments"
    id = Column(Integer, primary_key=True, index=True)
    segment_name = Column(String, index=True)
    length = Column(Float)
    width = Column(Float)
    pavement_type = Column(String)

class RoadSegment(BaseModel):
    segment_name: str
    length: float
    width: float
    pavement_type: str

    model_config = ConfigDict(from_attributes=True)
