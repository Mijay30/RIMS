from datetime import datetime
from ..database.connection import Database

class LifecycleService:
    def __init__(self):
        self.db = Database.connect()

    def resolve_incident(self, incident_id: str):
        # 1. Marcam incidentul ca rezolvat si punem timestamp
        self.db.incidents.update_one(
            {"incidentId": incident_id},
            {"$set": {
                "status": "Resolved",
                "resolvedAt": datetime.now().isoformat()
            }}
        )
        
        # 2. Eliberam vehiculul asociat (daca exista)
        # Cautam in colectia de interventii/alocari
        allocation = self.db.allocations.find_one({"incidentId": incident_id})
        if allocation:
            reg_number = allocation.get("vehicleRegistration")
            self.db.vehicles.update_one(
                {"registrationNumber": reg_number},
                {"$set": {"status": "Available"}}
            )
        
        return {"status": "success", "message": f"Incidentul {incident_id} a fost finalizat."}