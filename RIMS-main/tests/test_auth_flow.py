import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

@patch('app.main.SessionLocal')
@patch('app.main.verify_password')
def test_successful_login_and_access(mock_verify_password, mock_session):
    """Testează obținerea unui token JWT și accesarea unei rute protejate."""
    
    # 1. Configurare Bază de Date Mock pentru a simula un utilizator 'Staff'
    mock_db = MagicMock()
    mock_session.return_value = mock_db
    
    mock_user = MagicMock()
    mock_user.username = "staff"
    mock_user.role = "Staff"
    mock_user.hashed_password = "hashed_password"
    
    # Simulăm rezultatul căutării utilizatorului în baza de date
    mock_db.query().filter().first.return_value = mock_user
    # Simulăm că parola introdusă este corectă
    mock_verify_password.return_value = True

    # 2. Executăm request-ul de Login
    response = client.post("/token", data={"username": "staff", "password": "staff123"})
    assert response.status_code == 200
    
    # Extragem Token-ul din răspuns
    token = response.json().get("access_token")
    assert token is not None

    # 3. Executăm request către un endpoint protejat folosind Token-ul obținut
    headers = {"Authorization": f"Bearer {token}"}
    protected_response = client.get("/team-members", headers=headers)
    assert protected_response.status_code == 200