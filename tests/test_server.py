import pytest
from fastapi.testclient import TestClient
import yaml
from src.main import app, canvases

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_canvases():
    """Clear the canvases dictionary before each test."""
    canvases.clear()
    yield
    canvases.clear()

def test_create_canvas():
    """Test creating a new canvas."""
    test_data = {"type": "rect", "width": 100, "height": 50}
    response = client.post(
        "/canvas",
        content=yaml.dump(test_data),
        headers={"Content-Type": "application/yaml"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["data"] == test_data
    assert "jsCode" in data

def test_create_canvas_invalid_yaml():
    """Test creating a canvas with invalid YAML."""
    response = client.post(
        "/canvas",
        content="invalid: yaml: content: - [",
        headers={"Content-Type": "application/yaml"}
    )
    assert response.status_code == 400
    assert "error" in response.json()

def test_list_canvases_empty():
    """Test listing canvases when none exist."""
    response = client.get("/canvas")
    assert response.status_code == 200
    assert response.json() == []

def test_list_canvases():
    """Test listing canvases when some exist."""
    # Create a canvas first
    test_data = {"type": "circle", "radius": 30}
    create_response = client.post(
        "/canvas",
        content=yaml.dump(test_data),
        headers={"Content-Type": "application/yaml"}
    )
    canvas_id = create_response.json()["id"]
    
    # Now list canvases
    response = client.get("/canvas")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == canvas_id
    assert data[0]["data"] == test_data

def test_get_canvas():
    """Test getting a specific canvas by ID."""
    # Create a canvas first
    test_data = {"type": "line", "points": [10, 10, 20, 20]}
    create_response = client.post(
        "/canvas",
        content=yaml.dump(test_data),
        headers={"Content-Type": "application/yaml"}
    )
    canvas_id = create_response.json()["id"]
    
    # Now get the canvas
    response = client.get(f"/canvas/{canvas_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == canvas_id
    assert data["data"] == test_data

def test_get_canvas_not_found():
    """Test getting a canvas that doesn't exist."""
    response = client.get("/canvas/nonexistent-id")
    assert response.status_code == 404
    assert "detail" in response.json()

def test_update_canvas():
    """Test updating an existing canvas."""
    # Create a canvas first
    original_data = {"type": "rect", "width": 100, "height": 50}
    create_response = client.post(
        "/canvas",
        content=yaml.dump(original_data),
        headers={"Content-Type": "application/yaml"}
    )
    canvas_id = create_response.json()["id"]
    
    # Now update the canvas
    updated_data = {"type": "rect", "width": 200, "height": 75}
    response = client.put(
        f"/canvas/{canvas_id}",
        content=yaml.dump(updated_data),
        headers={"Content-Type": "application/yaml"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == canvas_id
    assert data["data"] == updated_data
    assert "jsCode" in data

def test_update_canvas_not_found():
    """Test updating a canvas that doesn't exist."""
    test_data = {"type": "rect", "width": 100, "height": 50}
    response = client.put(
        "/canvas/nonexistent-id",
        content=yaml.dump(test_data),
        headers={"Content-Type": "application/yaml"}
    )
    assert response.status_code == 404
    assert "detail" in response.json()

def test_update_canvas_invalid_yaml():
    """Test updating a canvas with invalid YAML."""
    # Create a canvas first
    original_data = {"type": "rect", "width": 100, "height": 50}
    create_response = client.post(
        "/canvas",
        content=yaml.dump(original_data),
        headers={"Content-Type": "application/yaml"}
    )
    canvas_id = create_response.json()["id"]
    
    # Now try to update with invalid YAML
    response = client.put(
        f"/canvas/{canvas_id}",
        content="invalid: yaml: content: - [",
        headers={"Content-Type": "application/yaml"}
    )
    assert response.status_code == 400
    assert "error" in response.json()

def test_delete_canvas():
    """Test deleting a canvas."""
    # Create a canvas first
    test_data = {"type": "circle", "radius": 30}
    create_response = client.post(
        "/canvas",
        content=yaml.dump(test_data),
        headers={"Content-Type": "application/yaml"}
    )
    canvas_id = create_response.json()["id"]
    
    # Now delete the canvas
    response = client.delete(f"/canvas/{canvas_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == canvas_id
    assert data["message"] == "Canvas deleted successfully"
    assert data["data"] == test_data
    
    # Verify it's gone
    get_response = client.get(f"/canvas/{canvas_id}")
    assert get_response.status_code == 404

def test_delete_canvas_not_found():
    """Test deleting a canvas that doesn't exist."""
    response = client.delete("/canvas/nonexistent-id")
    assert response.status_code == 404
    assert "detail" in response.json()

def test_custom_openapi():
    """Test the custom OpenAPI schema endpoint."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "info" in data, "OpenAPI schema missing info object"
    assert data["info"]["title"] == "KonvaJS Canvas API"
    assert data["info"]["version"] == "konva/v9.2.0"
