from typing import List, Optional
from ..database.connection import Database

class SearchService:
    def __init__(self):
        self.db = Database.connect()

    def search_vehicles(self, vehicle_type: Optional[str] = None, status: Optional[str] = None):
        query = {}
        if vehicle_type:
            query["vehicleType"] = vehicle_type
        if status:
            query["status"] = status
        
        return list(self.db.vehicles.find(query, {"_id": 0}))

    def search_incidents(self, incident_type: Optional[str] = None, status: Optional[str] = None):
        query = {}
        if incident_type:
            query["incidentType"] = incident_type
        if status:
            query["status"] = status
            
        return list(self.db.incidents.find(query, {"_id": 0}))