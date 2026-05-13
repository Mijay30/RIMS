import math
from ..models.vehicle import VehicleSQL
from ..models.incident import IncidentSQL
from ..database.connection import SessionLocal

class AllocationService:
    def get_suggestions(self, incident_id: int):
        db = SessionLocal()
        try:
            incident = db.query(IncidentSQL).filter(IncidentSQL.id == incident_id).first()
            if not incident:
                return []

            available_vehicles = db.query(VehicleSQL).filter(
                VehicleSQL.availability_status == "Available"
            ).all()

            suggestions = []
            for vehicle in available_vehicles:
                if vehicle.latitude is not None and vehicle.longitude is not None:
                    distance = math.sqrt(
                        (vehicle.latitude - incident.latitude)**2 + 
                        (vehicle.longitude - incident.longitude)**2
                    )
                    suggestions.append({
                        "vehicle_id": vehicle.id,
                        "registration_number": vehicle.registration_number,
                        "vehicle_type": vehicle.vehicle_type,
                        "distance": round(distance, 4)
                    })
            
            suggestions.sort(key=lambda x: x["distance"])
            return suggestions
        finally:
            db.close()

    def allocate_resource(self, incident_id: int, vehicle_id: int):
        db = SessionLocal()
        try:
            incident = db.query(IncidentSQL).filter(IncidentSQL.id == incident_id).first()
            vehicle = db.query(VehicleSQL).filter(VehicleSQL.id == vehicle_id).first()

            if not incident or not vehicle:
                return {"success": False, "message": "Incident or Vehicle not found"}

            if vehicle.availability_status != "Available":
                return {"success": False, "message": "Vehicle is not available"}

            incident.status = "Assigned"
            incident.assigned_vehicle_id = str(vehicle.id)
            vehicle.availability_status = "Busy"
            
            db.commit()
            return {
                "success": True, 
                "message": f"Vehicle {vehicle.registration_number} allocated to incident {incident_id}",
                "incident_id": incident_id,
                "vehicle_id": vehicle_id
            }
        except Exception as e:
            db.rollback()
            return {"success": False, "message": str(e)}
        finally:
            db.close()
