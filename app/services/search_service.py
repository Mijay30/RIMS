from ..database.connection import SessionLocal
from ..models.incident import IncidentSQL

class SearchService:
    def __init__(self):
        pass

    def search_incidents(self, incident_type: str = None, status: str = None):
        db = SessionLocal()
        try:
            query = db.query(IncidentSQL)
            if incident_type:
                query = query.filter(IncidentSQL.hazard_type == incident_type)
            if status:
                query = query.filter(IncidentSQL.status == status)
            incidents = query.all()
            return [
                {
                    "id": inc.id,
                    "hazard_type": inc.hazard_type,
                    "description": inc.description,
                    "latitude": inc.latitude,
                    "longitude": inc.longitude,
                    "status": inc.status,
                    "created_at": inc.created_at.isoformat() if inc.created_at else None
                }
                for inc in incidents
            ]
        finally:
            db.close()

    def search_vehicles(self, vehicle_type: str = None, status: str = None):
        return []
