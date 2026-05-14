import io
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .models.vehicle import Vehicle, VehicleSQL, VehicleTypeSQL, VehicleType
from .models.incident import IncidentReport, Incident, IncidentSQL
from .models.team import TeamMemberSQL, TeamMemberCreate, TeamMemberUpdate
from .services.allocation import AllocationService
from .database.connection import Database, Base, engine, SessionLocal
from .services.search_service import SearchService
from .services.reporting_service import ReportingService
from .services.export_service import ExportService
from .services.lifecycle_service import LifecycleService
from .services.priority_service import PriorityService
from .services.gis_service import GISService

app = FastAPI(title="Roads Infrastructure Management System (RIMS)")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="frontend/templates")

gis_svc = GISService()
lifecycle_svc = LifecycleService()
priority_svc = PriorityService()
allocation_service = AllocationService()
search_service = SearchService()
reporting_service = ReportingService()
export_service = ExportService()

@app.on_event("startup")
async def startup_db_client():
    Database.connect()
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(VehicleTypeSQL).first():
            for t in VehicleType:
                db.add(VehicleTypeSQL(name=t.value))
            db.commit()
        
        if not db.query(TeamMemberSQL).first():
            members = [
                TeamMemberSQL(full_name="Alice Johnson", certification_level="Senior", availability_status="Active", department="Maintenance"),
                TeamMemberSQL(full_name="Bob Smith", certification_level="Junior", availability_status="Active", department="Logistics"),
                TeamMemberSQL(full_name="Charlie Brown", certification_level="Senior", availability_status="Inactive", department="Engineering")
            ]
            db.add_all(members)
            db.commit()
    finally:
        db.close()

@app.get("/team-members")
async def get_team_members():
    db = SessionLocal()
    try:
        members = db.query(TeamMemberSQL).all()
        return members
    finally:
        db.close()

@app.post("/team-members")
async def create_team_member(member: TeamMemberCreate):
    db = SessionLocal()
    try:
        new_member = TeamMemberSQL(**member.dict())
        db.add(new_member)
        db.commit()
        db.refresh(new_member)
        return new_member
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@app.patch("/team-members/{member_id}")
async def update_member_status(member_id: int, update: TeamMemberUpdate):
    db = SessionLocal()
    try:
        member = db.query(TeamMemberSQL).filter(TeamMemberSQL.id == member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        member.availability_status = update.availability_status
        db.commit()
        db.refresh(member)
        return member
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@app.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse(request=request, name="map.html")

@app.get("/map", include_in_schema=False)
async def get_map(request: Request):
    return templates.TemplateResponse(request=request, name='map.html', context={})

@app.get("/admin")
async def get_admin(request: Request):
    return templates.TemplateResponse(request=request, name="admin_dashboard.html")

@app.get("/admin/stats")
async def get_admin_stats():
    db = SessionLocal()
    try:
        vehicles = db.query(VehicleSQL).all()
        active_units = sum(1 for v in vehicles if v.availability_status != "Maintenance")
        under_maintenance = sum(1 for v in vehicles if v.availability_status == "Maintenance")
        
        available_capacity = 0
        for v in vehicles:
            if v.availability_status == "Available":
                try:
                    available_capacity += float(v.capacity.replace('kg', ''))
                except (ValueError, TypeError, AttributeError):
                    pass
        
        type_dist = {}
        for v in vehicles:
            v_type = v.vehicle_type or "Unknown"
            type_dist[v_type] = type_dist.get(v_type, 0) + 1
            
        return {
            "active_units": active_units,
            "under_maintenance": under_maintenance,
            "available_capacity": available_capacity,
            "type_distribution": type_dist
        }
    finally:
        db.close()

@app.get("/vehicle-types")
async def list_vehicle_types():
    db = SessionLocal()
    try:
        types = db.query(VehicleTypeSQL).all()
        return [t.name for t in types]
    finally:
        db.close()

@app.post("/vehicle-types")
async def add_vehicle_type(name: str):
    db = SessionLocal()
    try:
        new_type = VehicleTypeSQL(name=name)
        db.add(new_type)
        db.commit()
        return {"name": name}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@app.post("/reports")
async def create_report(incident: Incident):
    return gis_svc.save_report(incident.dict())

@app.post("/incidents/{incident_id}/resolve")
async def resolve_incident(incident_id: int):
    return lifecycle_svc.resolve_incident(incident_id)

@app.post("/incidents/{incident_id}/advance")
async def advance_incident_status(incident_id: int):
    result = lifecycle_svc.advance_status(incident_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.get("/incidents/{incident_id}/suggestions")
async def get_incident_suggestions(incident_id: int):
    return allocation_service.get_suggestions(incident_id)

@app.post("/incidents/{incident_id}/allocate")
async def allocate_incident_resource(incident_id: int, vehicle_id: int):
    result = allocation_service.allocate_resource(incident_id, vehicle_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.get("/interventions")
async def get_interventions():
    return search_service.search_incidents()

@app.get("/fleet/status")
async def get_fleet_status():
    db = Database.connect()
    vehicles = list(db.vehicles.find({}, {"_id": 0}))
    return {"fleet": vehicles}

@app.get("/fleet/nodes")
async def get_fleet_nodes():
    db = SessionLocal()
    try:
        vehicles = db.query(VehicleSQL).all()
        return [
            {
                "id": v.id,
                "registration_number": v.registration_number,
                "vehicle_type": v.vehicle_type,
                "capacity": v.capacity,
                "equipment_type": v.equipment_type,
                "availability_status": v.availability_status,
                "maintenance_status": v.maintenance_status,
                "maintenance_history": v.maintenance_history,
                "assigned_team_id": v.assigned_team_id,
                "status": v.status
            }
            for v in vehicles
        ]
    finally:
        db.close()

@app.get("/search/vehicles")
async def search_vehicles(type: str = None, status: str = None):
    return search_service.search_vehicles(vehicle_type=type, status=status)

@app.get("/search/incidents")
async def search_incidents(type: str = None, status: str = None):
    return search_service.search_incidents(incident_type=type, status=status)

@app.get("/analytics/summary")
async def get_analytics_summary():
    return {
        "incident_stats": reporting_service.get_incident_statistics(),
        "avg_response_time_hours": reporting_service.calculate_average_response_time(),
        "fleet_overview": reporting_service.get_fleet_utilization_report()
    }

@app.get("/export/incidents/csv")
async def export_incidents():
    csv_data = export_service.export_incidents_to_csv()
    return StreamingResponse(
        io.StringIO(csv_data),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=incidents_report.csv"}
    )
