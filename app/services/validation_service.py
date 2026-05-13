from typing import Dict, List
from ..database.connection import Database
from ..models.incident import Coordinates

class ValidationService:
    def __init__(self):
        self.db = Database.connect()

    def is_duplicate_incident(self, coords: Coordinates, radius_km: float = 0.05) -> bool:


        active_incidents = self.db.incidents.find({"status": {"$ne": "Resolved"}})
        
        for inc in active_incidents:
            loc = inc.get("location", {})
            lat_diff = abs(loc.get("latitude", 0) - coords.latitude)
            lon_diff = abs(loc.get("longitude", 0) - coords.longitude)

            if lat_diff < 0.0005 and lon_diff < 0.0005:
                return True
        return False

    def validate_road_condition_logic(self, sector_id: str, reported_condition: str) -> bool:
        sector = self.db.road_sectors.find_one({"sectorId": sector_id})
        if not sector:
            return True # Dacă sectorul nu există, nu putem valida logic


        current_grade = sector.get("conditionGrade", "Unknown")
        return not (current_grade == "Excellent" and reported_condition == "Critical")