from datetime import datetime
from ..database.connection import Database
from ..models.vehicle import VehicleStatus
from ..models.incident import IncidentStatus

class AllocationService:
    def __init__(self):
        self.db = Database.connect()

    def allocate_resource(self, incident_id: str, vehicle_id: str, staff_id: str):
        vehicle = self.db.vehicles.find_one({"_id": vehicle_id})
        
        if not vehicle or vehicle.get("status") != VehicleStatus.AVAILABLE:
            return {"success": False, "message": "Resource unavailable or does not exist"}

        fingerprint = {
            "modifiedBy": staff_id,
            "timestamp": datetime.now()
        }

        self.db.incidents.update_one(
            {"_id": incident_id},
            {
                "$set": {
                    "status": IncidentStatus.ASSIGNED,
                    "assignedVehicleId": vehicle_id,
                    "lastModifiedBy": staff_id,
                    "updatedAt": datetime.now(),
                    "fingerprint": fingerprint
                }
            }
        )

        self.db.vehicles.update_one(
            {"_id": vehicle_id},
            {
                "$set": {
                    "status": VehicleStatus.BUSY,
                    "updatedAt": datetime.now()
                }
            }
        )

        return {"success": True, "details": "Resource allocated successfully"}