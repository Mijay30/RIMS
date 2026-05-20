import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_login_page():
    """Testează dacă pagina de login este încărcată cu succes."""
    response = client.get("/login")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_read_root():
    """Testează redirectul implicit (rădăcina returnează login.html)."""
    response = client.get("/")
    assert response.status_code == 200

def test_unauthorized_access_redirects_to_login():
    """Testează interceptarea erorii 401 din auth_exception_handler."""
    response = client.get("/admin-dashboard")
    assert response.status_code == 200
    assert "login" in str(response.url)

def test_login_invalid_credentials():
    """Testează blocarea unui request de autentificare invalid."""
   
    response = client.post("/token", data={"username": "wronguser", "password": "wrongpassword"}, follow_redirects=False)
    assert response.status_code in [302, 303, 307]
    assert response.headers.get("location") == "/login"