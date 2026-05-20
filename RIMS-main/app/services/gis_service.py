from typing import Dict, List
from ..models.incident import Coordinates, IncidentSQL
from ..database import SessionLocal

class GISService:
    def __init__(self, provider: str = "OpenStreetMap"):
        self.provider = provider

    def format_coordinates(self, lat: float, lon: float) -> Dict[str, float]:
        return {
            "latitude": round(lat, 6),
            "longitude": round(lon, 6)
        }

    def get_map_marker_metadata(self, incident_id: str, location: Coordinates) -> Dict:
        return {
            "incidentId": incident_id,
            "lat": location.latitude,
            "lng": location.longitude,
            "icon": "hazard_pin",
            "popupContent": f"Incident ID: {incident_id}"
        }

    def validate_spatial_bounds(self, coords: Coordinates) -> bool:
        if not (-90 <= coords.latitude <= 90) or not (-180 <= coords.longitude <= 180):
            return False
        return True

    def save_report(self, data: Dict) -> Dict:
        db = SessionLocal()
        try:
            coords = self.format_coordinates(data['latitude'], data['longitude'])
            new_incident = IncidentSQL(
                hazard_type=data['hazard_type'],
                description=data['description'],
                latitude=coords['latitude'],
                longitude=coords['longitude']
            )
            db.add(new_incident)
            db.commit()
            db.refresh(new_incident)
            return {
                "status": "success", 
                "message": "Report saved", 
                "id": new_incident.id,
                "hazard_type": new_incident.hazard_type,
                "description": new_incident.description,
                "latitude": new_incident.latitude,
                "longitude": new_incident.longitude,
                "status": new_incident.status,
                "created_at": new_incident.created_at.isoformat() if new_incident.created_at else None,
                "last_modified": new_incident.last_modified.isoformat() if new_incident.last_modified else None
            }
        finally:
            db.close()
