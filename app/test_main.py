from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_list_maker():
    response = client.get("/v2/maker")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}