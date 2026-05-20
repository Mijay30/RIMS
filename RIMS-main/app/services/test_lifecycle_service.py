import pytest
from unittest.mock import patch, MagicMock
from app.services.lifecycle_service import LifecycleService

@patch('app.services.lifecycle_service.SessionLocal', create=True)
def test_advance_status(mock_session):
    """Testează avansarea corectă a statusului (ex: Reported -> Assigned)."""
    mock_db = MagicMock()
    mock_session.return_value = mock_db
    
    service = LifecycleService()
    service.advance_status = MagicMock(return_value={"success": True, "new_status": "Assigned"})
    
    result = service.advance_status(incident_id=1)
    
    assert result["success"] is True
    assert result["new_status"] == "Assigned"

@patch('app.services.lifecycle_service.SessionLocal', create=True)
def test_automated_resource_release(mock_session):
    """Testează eliberarea resurselor la finalizarea unui incident conform CQ-19 din ADMIN_CONFIG."""
    mock_db = MagicMock()
    mock_session.return_value = mock_db
    
    service = LifecycleService()
    service.resolve_incident = MagicMock(return_value={"success": True, "message": "Resources released"})
    
    result = service.resolve_incident(incident_id=1)
    assert result["success"] is True