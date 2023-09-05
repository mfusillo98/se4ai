from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_project():
    response = client.post(
        "/api/projects/create",
        json={"name": "Test project", "selected_features_index": []}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['status'] == "OK"
    assert response_json['project_id'] is not None
    assert response_json['api_key'] is not None
