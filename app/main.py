from fastapi import FastAPI, HTTPException
from .models.vehicle import Vehicle
from .models.incident import IncidentReport
from .services.allocation import AllocationService
from .database.connection import Database

app = FastAPI(title="Roads Infrastructure Management System (RIMS)")
allocation_service = AllocationService()

@app.on_event("startup")
async def startup_db_client():
    Database.connect()

@app.post("/reports/add")
async def report_incident(incident: IncidentReport):
    db = Database.connect()
    result = db.incidents.insert_one(incident.dict())
    return {"id": str(result.inserted_id), "status": "Reported"}

@app.post("/interventions/allocate")
async def allocate_intervention(incident_id: str, vehicle_id: str, staff_id: str):
    result = allocation_service.allocate_resource(incident_id, vehicle_id, staff_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.get("/fleet/status")
async def get_fleet_status():
    db = Database.connect()
    vehicles = list(db.vehicles.find({}, {"_id": 0}))
    return {"fleet": vehicles}