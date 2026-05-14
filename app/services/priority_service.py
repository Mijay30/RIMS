from typing import Dict
from ..database import Database

class PriorityService:
    def __init__(self):
        self.db = Database.connect()

    def calculate_priority_score(self, incident_type: str, road_grade: str) -> int:
        type_weights = {
            "Flooding": 10,
            "Pothole": 7,
            "Faded Markings": 3,
            "Debris": 5
        }
        
        grade_weights = {
            "Critical": 10,
            "Poor": 7,
            "Fair": 4,
            "Excellent": 1
        }
        
        score = type_weights.get(incident_type, 1) + grade_weights.get(road_grade, 1)
        return score

    def update_incident_priority(self, incident_id: str):
        incident = self.db.incidents.find_one({"incidentId": incident_id})
        sector = self.db.road_sectors.find_one({"sectorId": incident.get("sectorId")})
        
        if incident and sector:
            score = self.calculate_priority_score(
                incident["incidentType"], 
                sector["conditionGrade"]
            )
            self.db.incidents.update_one(
                {"incidentId": incident_id},
                {"$set": {"priorityScore": score}}
            )