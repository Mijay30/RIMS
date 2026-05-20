import io
import os
from fastapi import FastAPI, HTTPException, Request, Depends, status, Response
from fastapi.responses import StreamingResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from .auth import get_current_user, create_access_token, require_user_role, require_staff_role, require_admin_role, verify_password, get_password_hash
from .models.vehicle import Vehicle, VehicleSQL, VehicleTypeSQL, VehicleType
from .models.incident import IncidentReport, Incident, IncidentSQL, IncidentStatus
from app.models.incident import IncidentStatus
from .models.team import TeamMemberSQL, TeamMemberCreate, TeamMemberUpdate
from .models.auth import UserSQL
from .models.road_inventory import RoadSegmentSQL
from .services.allocation import AllocationService
from .database import Database, Base, engine, SessionLocal, init_db
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

@app.exception_handler(HTTPException)
async def auth_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return RedirectResponse(url="/login")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.on_event("startup")
async def startup_db_client():
    init_db()
    db = SessionLocal()
    try:
        if not db.query(VehicleTypeSQL).first():
            for t in VehicleType:
                db.add(VehicleTypeSQL(name=t.value))
            db.commit()
        
        if not db.query(UserSQL).first():
            users = [
                UserSQL(username="admin", hashed_password=get_password_hash("admin123"), role="Admin", email="admin@rims.com"),
                UserSQL(username="staff", hashed_password=get_password_hash("staff123"), role="Staff", email="staff@rims.com"),
                UserSQL(username="user", hashed_password=get_password_hash("user123"), role="User", email="user@rims.com")
            ]
            db.add_all(users)
            db.commit()

        if not db.query(RoadSegmentSQL).first():
            segments = [
                RoadSegmentSQL(segment_name="Calea Bucuresti", length=5.2, width=12.0, pavement_type="Asphalt"),
                RoadSegmentSQL(segment_name="Nicolae Titulescu", length=3.1, width=10.0, pavement_type="Asphalt"),
                RoadSegmentSQL(segment_name="Calea Unirii", length=2.5, width=8.0, pavement_type="Stone")
            ]
            db.add_all(segments)
            db.commit()

        if not db.query(VehicleSQL).first():
            vehicles = [
                VehicleSQL(registration_number="B-101-ASPH", vehicle_type=VehicleType.ASPHALT_LAYING.value, capacity="5000kg", equipment_type="Spreader", availability_status="Available", maintenance_status="Good", maintenance_history="New vehicle", status="Available"),
                VehicleSQL(registration_number="B-102-ASPH", vehicle_type=VehicleType.ASPHALT_LAYING.value, capacity="5000kg", equipment_type="Spreader", availability_status="Available", maintenance_status="Good", maintenance_history="New vehicle", status="Available"),
                VehicleSQL(registration_number="B-202-SNOW", vehicle_type=VehicleType.SNOW_REMOVAL.value, capacity="3000kg", equipment_type="Plow", availability_status="Available", maintenance_status="Good", maintenance_history="New vehicle", status="Available"),
                VehicleSQL(registration_number="B-303-PATH", vehicle_type=VehicleType.POTHOLE_REPAIR.value, capacity="2000kg", equipment_type="Thermal patcher", availability_status="Available", maintenance_status="Good", maintenance_history="New vehicle", status="Available")
            ]
            db.add_all(vehicles)
            db.commit()

        if not db.query(TeamMemberSQL).first():
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
    finally:
        db.close()

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    try:
        user = db.query(UserSQL).filter(UserSQL.username == form_data.username).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(data={"sub": user.username, "role": user.role.lower()})
        response = JSONResponse(content={"access_token": access_token, "token_type": "bearer", "role": user.role.lower()})
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response
    finally:
        db.close()

@app.get("/login")
async def get_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/map", include_in_schema=False)
async def get_map(request: Request, current_user: dict = Depends(require_user_role)):
    return templates.TemplateResponse(request=request, name='map.html', context={"user": current_user})

@app.get("/admin-dashboard")
async def get_admin(request: Request, current_user: dict = Depends(require_staff_role)):
    return templates.TemplateResponse(request=request, name="admin_dashboard.html", context={"user": current_user})

@app.get("/team-members")
async def get_team_members(current_user: dict = Depends(require_staff_role)):
    db = SessionLocal()
    try:
        members = db.query(TeamMemberSQL).all()
        return members
    finally:
        db.close()

@app.post("/team-members")
async def create_team_member(member: TeamMemberCreate, current_user: dict = Depends(require_admin_role)):
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
async def update_member_status(member_id: int, update: TeamMemberUpdate, current_user: dict = Depends(require_admin_role)):
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

@app.get("/admin/stats")
async def get_admin_stats(current_user: dict = Depends(require_staff_role)):
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
async def list_vehicle_types(current_user: dict = Depends(require_staff_role)):
    db = SessionLocal()
    try:
        types = db.query(VehicleTypeSQL).all()
        return [t.name for t in types]
    finally:
        db.close()

@app.post("/vehicle-types")
async def add_vehicle_type(name: str, current_user: dict = Depends(require_admin_role)):
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
async def create_report(incident: Incident, current_user: dict = Depends(require_user_role)):
    return gis_svc.save_report(incident.dict())

@app.post("/incidents/{incident_id}/resolve")
async def resolve_incident(incident_id: int, current_user: dict = Depends(require_staff_role)):
    return lifecycle_svc.resolve_incident(incident_id)

@app.post("/incidents/{incident_id}/advance")
async def advance_incident_status(incident_id: int, current_user: dict = Depends(require_staff_role)):
    result = lifecycle_svc.advance_status(incident_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.get("/incidents/{incident_id}/suggestions")
async def get_incident_suggestions(incident_id: int, current_user: dict = Depends(require_staff_role)):
    return allocation_service.get_suggestions(incident_id)

@app.post("/incidents/{incident_id}/allocate")
async def allocate_incident_resource(incident_id: int, vehicle_id: int, current_user: dict = Depends(require_staff_role)):
    result = allocation_service.allocate_resource(incident_id, vehicle_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.get("/interventions")
async def get_interventions(current_user: dict = Depends(require_user_role)):
    return search_service.search_incidents()

@app.get("/fleet/status")
async def get_fleet_status(current_user: dict = Depends(require_staff_role)):
    db = Database.connect()
    vehicles = list(db.vehicles.find({}, {"_id": 0}))
    return {"fleet": vehicles}

@app.get("/fleet/nodes")
async def get_fleet_nodes(current_user: dict = Depends(require_staff_role)):
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
async def search_vehicles(type: str = None, status: str = None, current_user: dict = Depends(require_staff_role)):
    return search_service.search_vehicles(vehicle_type=type, status=status)

@app.get("/search/incidents")
async def search_incidents(type: str = None, status: str = None, current_user: dict = Depends(require_staff_role)):
    return search_service.search_incidents(incident_type=type, status=status)

@app.get("/analytics/summary")
async def get_analytics_summary(current_user: dict = Depends(require_staff_role)):
    return {
        "incident_stats": reporting_service.get_incident_statistics(),
        "avg_response_time_hours": reporting_service.calculate_average_response_time(),
        "fleet_overview": reporting_service.get_fleet_utilization_report()
    }

@app.get("/export/incidents/csv")
async def export_incidents(current_user: dict = Depends(require_staff_role)):
    csv_data = export_service.export_incidents_to_csv()
    return StreamingResponse(
        io.StringIO(csv_data),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=incidents_report.csv"}
    )

@app.get("/api/v1/analytics/report")
async def get_detailed_analytics_report(current_user: dict = Depends(require_staff_role)):
    db = SessionLocal()
    try:
        completed_incidents = db.query(IncidentSQL).filter(IncidentSQL.status == IncidentStatus.COMPLETED).all()
        if not completed_incidents:
            return {"average_resolution_time_seconds": 0, "count": 0}
        
        total_time = 0
        count = 0
        for inc in completed_incidents:
            if inc.completed_at and inc.created_at:
                diff = (inc.completed_at - inc.created_at).total_seconds()
                total_time += diff
                count += 1
        
        avg_time = total_time / count if count > 0 else 0
        return {
            "average_resolution_time_seconds": avg_time,
            "average_resolution_time_formatted": f"{avg_time/3600:.2f} hours",
            "count": count
        }
    finally:
        db.close()
