import os
import sys
from datetime import datetime

# Add the current directory to sys.path to import app modules
sys.path.append(os.getcwd())

from app.database.connection import engine, Base, SessionLocal
from app.models.vehicle import VehicleSQL, VehicleTypeSQL, VehicleType
from app.models.incident import IncidentSQL, IncidentStatus
from app.models.road_inventory import RoadSegmentSQL
from app.models.team import TeamMemberSQL

def reinit_db():
    db_file = "rims.db"
    if os.path.exists(db_file):
        print(f"Removing existing database file: {db_file}")
        os.remove(db_file)
    
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("Seeding road segments...")
        segments = [
            RoadSegmentSQL(segment_name="Calea Bucuresti", length=5.2, width=12.0, pavement_type="Asphalt"),
            RoadSegmentSQL(segment_name="Nicolae Titulescu", length=3.1, width=10.0, pavement_type="Asphalt"),
            RoadSegmentSQL(segment_name="Calea Unirii", length=2.5, width=8.0, pavement_type="Stone")
        ]
        db.add_all(segments)

        print("Seeding vehicle types...")
        for t in VehicleType:
            db.add(VehicleTypeSQL(name=t.value))
        
        print("Seeding sample vehicles...")
        vehicles = [
            VehicleSQL(
                registration_number="B-101-ASPH",
                vehicle_type=VehicleType.ASPHALT_LAYING.value,
                capacity="5000kg",
                equipment_type="Spreader",
                availability_status="Available",
                maintenance_status="Good",
                maintenance_history="New vehicle",
                status="Available",
                latitude=44.4300,
                longitude=26.1000,
                updated_at=datetime.now()
            ),
            VehicleSQL(
                registration_number="B-202-SNOW",
                vehicle_type=VehicleType.SNOW_REMOVAL.value,
                capacity="3000kg",
                equipment_type="Plow",
                availability_status="Available",
                maintenance_status="Good",
                maintenance_history="New vehicle",
                status="Available",
                latitude=44.4400,
                longitude=26.1100,
                updated_at=datetime.now()
            ),
            VehicleSQL(
                registration_number="B-303-PATH",
                vehicle_type=VehicleType.POTHOLE_REPAIR.value,
                capacity="2000kg",
                equipment_type="Thermal patcher",
                availability_status="Available",
                maintenance_status="Good",
                maintenance_history="New vehicle",
                status="Available",
                latitude=44.4200,
                longitude=26.0900,
                updated_at=datetime.now()
            )
        ]
        db.add_all(vehicles)

        print("Seeding sample incidents...")
        incidents = [
            IncidentSQL(
                hazard_type="Pothole",
                description="Large pothole in the middle of the road",
                latitude=44.4268,
                longitude=26.1025,
                status=IncidentStatus.REPORTED
            ),
            IncidentSQL(
                hazard_type="Fallen Tree",
                description="Tree blocking the sidewalk",
                latitude=44.4350,
                longitude=26.1100,
                status=IncidentStatus.REPORTED
            )
        ]
        db.add_all(incidents)

        print("Seeding sample team members...")
        members = [
            TeamMemberSQL(full_name="Alice Johnson", certification_level="Senior", availability_status="Active", is_available=True, department="Maintenance"),
            TeamMemberSQL(full_name="Bob Smith", certification_level="Junior", availability_status="Active", is_available=True, department="Logistics")
        ]
        db.add_all(members)

        db.commit()
        print("Database re-initialized and seeded successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reinit_db()
