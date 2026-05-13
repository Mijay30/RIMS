from datetime import datetime
from typing import List, Dict
from ..database.connection import Database

class ReportingService:
    def __init__(self):
        self.db = Database.connect()

    def get_incident_statistics(self) -> Dict:
        pipeline = [
            {"$group": {"_id": "$incidentType", "count": {"$sum": 1}}}
        ]
        results = list(self.db.incidents.aggregate(pipeline))
        return {item["_id"]: item["count"] for item in results}

    def calculate_average_response_time(self) -> float:
        resolved_incidents = list(self.db.incidents.find({"status": "Resolved"}))
        if not resolved_incidents:
            return 0.0

        total_time = 0
        count = 0

        for inc in resolved_incidents:
            if "createdAt" in inc and "resolvedAt" in inc:
                fmt = "%Y-%m-%dT%H:%M:%S"
                start = datetime.strptime(inc["createdAt"], fmt)
                end = datetime.strptime(inc["resolvedAt"], fmt)
                total_time += (end - start).total_seconds()
                count += 1

        return (total_time / count) / 3600 if count > 0 else 0.0

    def get_fleet_utilization_report(self) -> List[Dict]:
        return list(self.db.vehicles.find({}, {"registrationNumber": 1, "status": 1, "_id": 0}))