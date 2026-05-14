import logging
from datetime import datetime
from typing import Dict
from ..database import Database

class NotificationService:
    def __init__(self):
        self.db = Database.connect()
        self.logger = logging.getLogger("RIMS_Notifications")

    def notify_team_assignment(self, team_id: str, incident_id: str, vehicle_id: str):
        message = f"ALERTA: Echipa {team_id} a fost alocata incidentului {incident_id} cu vehiculul {vehicle_id}."

        self.logger.info(f"Email trimis catre echipa {team_id}: {message}")

        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "TEAM_ASSIGNMENT",
            "details": message,
            "teamId": team_id,
            "incidentId": incident_id
        }
        self.db.audit_logs.insert_one(audit_entry)
        return True

    def get_audit_trail(self, incident_id: str):
        return list(self.db.audit_logs.find({"incidentId": incident_id}, {"_id": 0}))