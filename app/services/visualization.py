from typing import List, Dict
from ..database.connection import Database

class FleetVisualizationService:
    def __init__(self):
        self.db = Database.connect()

    def generate_fleet_graph(self) -> Dict:
        vehicles = list(self.db.vehicles.find())
        teams = list(self.db.teams.find())
        incidents = list(self.db.incidents.find({"status": "Assigned"}))

        nodes = []
        edges = []

        for v in vehicles:
            nodes.append({
                "id": f"v_{v['registrationNumber']}",
                "label": v['registrationNumber'],
                "type": "vehicle",
                "status": v['status']
            })

        for t in teams:
            nodes.append({
                "id": f"t_{t['teamId']}",
                "label": t['name'],
                "type": "team",
                "status": t['availability']
            })

        for i in incidents:
            if "assignedVehicleId" in i:
                edges.append({
                    "from": f"v_{i['assignedVehicleId']}",
                    "to": f"incident_{i['_id']}",
                    "label": "Assigned To"
                })

        return {"nodes": nodes, "edges": edges}