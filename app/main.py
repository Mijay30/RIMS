import io
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .models.vehicle import Vehicle, VehicleSQL
from .models.incident import IncidentReport, Incident, IncidentSQL
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

@app.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse(request=request, name="map.html")

@app.get("/map", include_in_schema=False)
async def get_map(request: Request):
    return templates.TemplateResponse(request=request, name='map.html', context={})

@app.post("/reports")
async def create_report(incident: Incident):
    return gis_svc.save_report(incident.dict())

@app.post("/incidents/{incident_id}/resolve")
async def resolve_incident(incident_id: str):
    return lifecycle_svc.resolve_incident(incident_id)

@app.post("/interventions/allocate")
async def allocate_intervention(incident_id: str, vehicle_id: str, staff_id: str):
    result = allocation_service.allocate_resource(incident_id, vehicle_id, staff_id)
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
