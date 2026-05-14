import os
import sys
from datetime import datetime

# Add the current directory to sys.path to import app modules
sys.path.append(os.getcwd())

from app.database import engine, Base, SessionLocal
from app.models.vehicle import VehicleSQL, VehicleTypeSQL, VehicleType
from app.models.incident import IncidentSQL, IncidentStatus
from app.models.road_inventory import RoadSegmentSQL
from app.models.team import TeamMemberSQL
from app.models.auth import UserSQL
from app.auth import get_password_hash

def reinit_db():
    print("Initializing database...")
    
    # Instead of deleting the file, we drop all tables EXCEPT 'users'
    # and then recreate everything.
    db = SessionLocal()
    try:
        # Get all table names from metadata
        all_tables = Base.metadata.tables
        for table_name, table in all_tables.items():
            if table_name != "users":
                print(f"Dropping table: {table_name}")
                table.drop(bind=engine, checkfirst=True)
    except Exception as e:
        print(f"Warning during drop: {e}")
    finally:
        db.close()
    
    print("Creating all missing tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Seed Users if missing
        if not db.query(UserSQL).first():
            print("Seeding default users...")
            users = [
                UserSQL(username="admin", hashed_password=get_password_hash("admin123"), role="Admin", email="admin@rims.com"),
                UserSQL(username="staff", hashed_password=get_password_hash("staff123"), role="Staff", email="staff@rims.com"),
                UserSQL(username="user", hashed_password=get_password_hash("user123"), role="User", email="user@rims.com")
            ]
            db.add_all(users)

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
                registration_number="B-102-ASPH",
                vehicle_type=VehicleType.ASPHALT_LAYING.value,
                capacity="5000kg",
                equipment_type="Spreader",
                availability_status="Available",
                maintenance_status="Good",
                maintenance_history="New vehicle",
                status="Available",
                latitude=44.4310,
                longitude=26.1010,
                updated_at=datetime.now()
            ),
            VehicleSQL(
                registration_number="B-103-ASPH",
                vehicle_type=VehicleType.ASPHALT_LAYING.value,
                capacity="5000kg",
                equipment_type="Spreader",
                availability_status="Available",
                maintenance_status="Good",
                maintenance_history="New vehicle",
                status="Available",
                latitude=44.4320,
                longitude=26.1020,
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
                registration_number="B-203-SNOW",
                vehicle_type=VehicleType.SNOW_REMOVAL.value,
                capacity="3000kg",
                equipment_type="Plow",
                availability_status="Available",
                maintenance_status="Good",
                maintenance_history="New vehicle",
                status="Available",
                latitude=44.4410,
                longitude=26.1110,
                updated_at=datetime.now()
            ),
            VehicleSQL(
                registration_number="B-204-SNOW",
                vehicle_type=VehicleType.SNOW_REMOVAL.value,
                capacity="3000kg",
                equipment_type="Plow",
                availability_status="Available",
                maintenance_status="Good",
                maintenance_history="New vehicle",
                status="Available",
                latitude=44.4420,
                longitude=26.1120,
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
            ),
            VehicleSQL(
                registration_number="B-404-REPAIR",
                vehicle_type="General Repair Van",
                capacity="1500kg",
                equipment_type="General Tools",
                availability_status="Available",
                maintenance_status="Good",
                maintenance_history="New vehicle",
                status="Available",
                latitude=44.4210,
                longitude=26.0910,
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
            TeamMemberSQL(full_name="Bob Smith", certification_level="Junior", availability_status="Active", is_available=True, department="Logistics"),
            TeamMemberSQL(full_name="Charlie Davis", certification_level="Expert", availability_status="Active", is_available=True, department="Engineering"),
            TeamMemberSQL(full_name="Diana Prince", certification_level="Intermediate", availability_status="Active", is_available=True, department="Operations"),
            TeamMemberSQL(full_name="Edward Norton", certification_level="Senior", availability_status="Active", is_available=True, department="Maintenance"),
            TeamMemberSQL(full_name="Fiona Gallagher", certification_level="Junior", availability_status="Active", is_available=True, department="Field Ops")
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
