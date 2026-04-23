from typing import Dict, List
from ..models.incident import Coordinates

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