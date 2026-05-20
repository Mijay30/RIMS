import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from app.services.maintenance_service import MaintenanceService

@patch('app.services.maintenance_service.Database.connect')
def test_check_fleet_health(mock_connect):
    """Testează identificarea vehiculelor a căror revizie tehnică a expirat."""
    mock_db = MagicMock()
    mock_connect.return_value = mock_db
    
    old_date = (datetime.now() - timedelta(days=200)).isoformat()
    recent_date = (datetime.now() - timedelta(days=10)).isoformat()
    
    mock_db.vehicles.find.return_value = [
        {"registrationNumber": "B-101-ASPH", "lastServiceDate": old_date},
        {"registrationNumber": "B-202-SNOW", "lastServiceDate": recent_date}
    ]
    
    service = MaintenanceService()
    flagged = service.check_fleet_health()
    
    assert len(flagged) == 1
    assert flagged[0] == "B-101-ASPH"
    
    mock_db.vehicles.update_one.assert_called_once_with(
        {"registrationNumber": "B-101-ASPH"},
        {"$set": {"status": "Under Maintenance"}}
    )

@patch('app.services.maintenance_service.Database.connect')
def test_complete_maintenance(mock_connect):
    """Testează completarea procesului de mentenanță."""
    mock_db = MagicMock()
    mock_connect.return_value = mock_db
    
    service = MaintenanceService()
    service.complete_maintenance("B-101-ASPH")
    
    mock_db.vehicles.update_one.assert_called_once()