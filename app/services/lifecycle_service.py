from datetime import datetime
from ..database.connection import SessionLocal
from ..models.incident import IncidentSQL, IncidentStatus
from .incident_service import IncidentService

class LifecycleService:
    def advance_status(self, incident_id: int):
        db = SessionLocal()
        try:
            incident = db.query(IncidentSQL).filter(IncidentSQL.id == incident_id).first()
            if not incident:
                return {"success": False, "message": "Incident not found"}
            
            current_status = incident.status
            next_status = IncidentService.get_next_status(current_status)
            
            if not next_status:
                return {"success": False, "message": "Incident already completed or invalid status"}
            
            if current_status == IncidentStatus.REPORTED:
                return {"success": False, "message": "Incident must be assigned a vehicle first"}

            incident.status = next_status
            if next_status == IncidentStatus.COMPLETED:
                incident.completed_at = datetime.now()
            db.commit()
            return {"success": True, "new_status": incident.status.value}
        except Exception as e:
            db.rollback()
            return {"success": False, "message": str(e)}
        finally:
            db.close()

    def resolve_incident(self, incident_id: int):
        db = SessionLocal()
        try:
            incident = db.query(IncidentSQL).filter(IncidentSQL.id == incident_id).first()
            if not incident:
                return {"success": False, "message": "Incident not found"}
            
            incident.status = IncidentStatus.COMPLETED
            incident.completed_at = datetime.now()
            db.commit()
            return {"status": "success", "message": f"Incident {incident_id} has been completed."}
        finally:
            db.close()
