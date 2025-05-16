from fastapi import FastAPI, Request, HTTPException, Path
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
import yaml
import uuid
from typing import Dict, List, Any, Optional

app = FastAPI()

# In-memory storage for canvas configurations
# In a production app, this would be a database
canvases: Dict[str, Dict[str, Any]] = {}

@app.post("/canvas")
async def create_canvas(request: Request):
    yaml_body = await request.body()
    try:
        data = yaml.safe_load(yaml_body)
        # Generate a unique ID for the canvas
        canvas_id = str(uuid.uuid4())
        canvases[canvas_id] = data
        
        # Simulate conversion to JS (actual logic omitted for brevity)
        js_code = f"// JS output for: {data}"
        
        return {
            "id": canvas_id,
            "jsCode": js_code,
            "data": data
        }
    except yaml.YAMLError as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.get("/canvas")
async def list_canvases():
    """List all canvas configurations."""
    result = []
    for canvas_id, data in canvases.items():
        result.append({
            "id": canvas_id,
            "data": data
        })
    return result

@app.get("/canvas/{canvas_id}")
async def get_canvas(canvas_id: str = Path(..., description="The ID of the canvas to retrieve")):
    """Get a specific canvas configuration by ID."""
    if canvas_id not in canvases:
        raise HTTPException(status_code=404, detail="Canvas not found")
    
    return {
        "id": canvas_id,
        "data": canvases[canvas_id]
    }

@app.put("/canvas/{canvas_id}")
async def update_canvas(
    request: Request,
    canvas_id: str = Path(..., description="The ID of the canvas to update")
):
    """Update an existing canvas configuration."""
    if canvas_id not in canvases:
        raise HTTPException(status_code=404, detail="Canvas not found")
    
    yaml_body = await request.body()
    try:
        data = yaml.safe_load(yaml_body)
        canvases[canvas_id] = data
        
        # Simulate conversion to JS
        js_code = f"// JS output for updated canvas: {data}"
        
        return {
            "id": canvas_id,
            "jsCode": js_code,
            "data": data
        }
    except yaml.YAMLError as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.delete("/canvas/{canvas_id}")
async def delete_canvas(canvas_id: str = Path(..., description="The ID of the canvas to delete")):
    """Delete a canvas configuration."""
    if canvas_id not in canvases:
        raise HTTPException(status_code=404, detail="Canvas not found")
    
    deleted_data = canvases.pop(canvas_id)
    
    return {
        "id": canvas_id,
        "message": "Canvas deleted successfully",
        "data": deleted_data
    }

# Optional: override OpenAPI schema
@app.get("/openapi.json", include_in_schema=False)
async def custom_openapi():
    return get_openapi(
        title="KonvaJS Canvas API",
        version="konva/v9.2.0",
        routes=app.routes,
    )
