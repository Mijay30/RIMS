from typing import List, Dict, Optional
from ..database.connection import Database
from ..models.road_sector import RoadSector

class RoadService:
    def __init__(self):
        self.db = Database.connect()

    def add_sector(self, sector: RoadSector) -> str:
        result = self.db.road_sectors.insert_one(sector.dict())
        return str(result.inserted_id)

    def get_all_sectors(self) -> List[Dict]:
        return list(self.db.road_sectors.find({}, {"_id": 0}))

    def get_sector_by_id(self, sector_id: str) -> Optional[Dict]:
        return self.db.road_sectors.find_one({"sectorId": sector_id}, {"_id": 0})

    def update_sector_condition(self, sector_id: str, new_condition: str):
        self.db.road_sectors.update_one(
            {"sectorId": sector_id},
            {"$set": {"conditionGrade": new_condition}}
        )