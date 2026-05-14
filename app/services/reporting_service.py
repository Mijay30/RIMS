from datetime import datetime
from typing import List, Dict
from ..database.connection import SessionLocal
from ..models.incident import IncidentSQL, IncidentStatus
from sqlalchemy import func

class ReportingService:
    def __init__(self):
        pass

    def get_incident_statistics(self) -> Dict:
        db = SessionLocal()
        try:
            results = db.query(IncidentSQL.hazard_type, func.count(IncidentSQL.id)).group_by(IncidentSQL.hazard_type).all()
            return {hazard_type: count for hazard_type, count in results}
        finally:
            db.close()

    def calculate_average_response_time(self) -> float:
        db = SessionLocal()
        try:
            completed_incidents = db.query(IncidentSQL).filter(IncidentSQL.status == IncidentStatus.COMPLETED).all()
            if not completed_incidents:
                return 0.0

            total_time = 0
            count = 0

            for inc in completed_incidents:
                if inc.created_at and inc.last_modified:
                    diff = (inc.last_modified - inc.created_at).total_seconds()
                    total_time += diff
                    count += 1

            return (total_time / count) / 3600 if count > 0 else 0.0
        finally:
            db.close()

    def get_fleet_utilization_report(self) -> List[Dict]:
        from ..models.vehicle import VehicleSQL
        db = SessionLocal()
        try:
            vehicles = db.query(VehicleSQL).all()
            return [
                {"registrationNumber": v.registration_number, "status": v.status}
                for v in vehicles
            ]
        finally:
            db.close()
