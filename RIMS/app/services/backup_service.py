import json
import os
from datetime import datetime
from ..database.connection import Database

class BackupService:
    def __init__(self):
        self.db = Database.connect()
        self.backup_path = "config/fleet_backup.json"

    def export_configuration(self):
        vehicles = list(self.db.vehicles.find({}, {"_id": 0}))
        teams = list(self.db.teams.find({}, {"_id": 0}))
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "vehicles": vehicles,
            "teams": teams
        }
        
        with open(self.backup_path, "w") as f:
            json.dump(data, f, indent=4)
        
        return self.backup_path

    def restore_configuration(self):
        if not os.path.exists(self.backup_path):
            return {"success": False, "message": "No backup file found"}
            
        try:
            with open(self.backup_path, "r") as f:
                data = json.load(f)
            
            self.db.vehicles.delete_many({})
            self.db.teams.delete_many({})
            
            if data["vehicles"]:
                self.db.vehicles.insert_many(data["vehicles"])
            if data["teams"]:
                self.db.teams.insert_many(data["teams"])
                
            return {"success": True, "message": "Configuration restored"}
        except (json.JSONDecodeError, KeyError) as e:
            return {"success": False, "message": f"Corrupted file: {str(e)}"}