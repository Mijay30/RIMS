from datetime import datetime, timedelta
from typing import List, Dict
from ..database.connection import Database

class MaintenanceService:
    def __init__(self):
        self.db = Database.connect()

    def check_fleet_health(self) -> List[str]:
        flagged_vehicles = []
        vehicles = list(self.db.vehicles.find())
        
        for v in vehicles:

            last_service = datetime.fromisoformat(v.get("lastServiceDate", datetime.now().isoformat()))
            if datetime.now() > last_service + timedelta(days=180):
                self.mark_for_maintenance(v["registrationNumber"])
                flagged_vehicles.append(v["registrationNumber"])
        
        return flagged_vehicles

    def mark_for_maintenance(self, registration_number: str):
        self.db.vehicles.update_one(
            {"registrationNumber": registration_number},
            {"$set": {"status": "Under Maintenance"}}
        )

    def complete_maintenance(self, registration_number: str):
        self.db.vehicles.update_one(
            {"registrationNumber": registration_number},
            {"$set": {
                "status": "Available",
                "lastServiceDate": datetime.now().isoformat()
            }}
        )