import json
import os
import sys
from datetime import datetime

# Add the root directory to sys.path to import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.database import SessionLocal
from app.models.vehicle import VehicleSQL
from app.models.team import TeamMemberSQL

def export_fleet_and_teams(output_file="fleet_backup.json"):
    db = SessionLocal()
    try:
        vehicles = db.query(VehicleSQL).all()
        team_members = db.query(TeamMemberSQL).all()

        data = {
            "exported_at": datetime.now().isoformat(),
            "fleet": [
                {
                    "registration_number": v.registration_number,
                    "vehicle_type": v.vehicle_type,
                    "capacity": v.capacity,
                    "equipment_type": v.equipment_type,
                    "status": v.status,
                    "is_available": v.is_available
                }
                for v in vehicles
            ],
            "teams": [
                {
                    "full_name": t.full_name,
                    "certification_level": t.certification_level,
                    "availability_status": t.availability_status,
                    "is_available": t.is_available,
                    "department": t.department
                }
                for t in team_members
            ]
        }

        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)
        
        print(f"Backup successfully exported to {output_file}")
    except Exception as e:
        print(f"Error during backup: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    export_fleet_and_teams()
