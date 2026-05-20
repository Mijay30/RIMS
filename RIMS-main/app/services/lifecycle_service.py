from datetime import datetime
from ..database import SessionLocal
from ..models.incident import IncidentSQL, IncidentStatus
from ..models.vehicle import VehicleSQL, VehicleStatus
from ..models.team import TeamMemberSQL
from .incident_service import IncidentService

class LifecycleService:
    def _release_resources(self, db, incident):
        """Helper to release vehicle and team members assigned to an incident."""
        if incident.assigned_vehicle_id:
            vehicle = db.query(VehicleSQL).filter(VehicleSQL.id == int(incident.assigned_vehicle_id)).first()
            if vehicle:
                vehicle.is_available = True
                vehicle.availability_status = "Available"
                vehicle.status = VehicleStatus.AVAILABLE
                
                if vehicle.assigned_team_id:
                    team_member_ids = vehicle.assigned_team_id.split(',')
                    for tm_id in team_member_ids:
                        if tm_id.strip():
                            member = db.query(TeamMemberSQL).filter(TeamMemberSQL.id == int(tm_id)).first()
                            if member:
                                member.is_available = True
                                member.availability_status = "Active"

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
            incident.last_modified = datetime.now()
            if next_status == IncidentStatus.COMPLETED:
                incident.completed_at = datetime.now()
                self._release_resources(db, incident)
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
            incident.last_modified = datetime.now()
            
            self._release_resources(db, incident)
            
            db.commit()
            return {"status": "success", "message": f"Incident {incident_id} has been completed."}
        except Exception as e:
            db.rollback()
            return {"success": False, "message": str(e)}
        finally:
            db.close()
