from fastapi import FastAPI, Request, HTTPException, Path
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
import yaml
import uuid
import json
from typing import Dict, List, Any, Optional

app = FastAPI()

# Add CORS middleware to allow requests from the web client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from web client
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

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
        
        # Generate actual executable JavaScript for Konva.js
        js_code = generate_konva_js(data)
        
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
        
        # Generate actual executable JavaScript for Konva.js
        js_code = generate_konva_js(data)
        
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

# Override OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="KonvaJS Canvas API",
        version="konva/v9.2.0",
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

def generate_konva_js(data):
    """Generate executable JavaScript code for Konva.js based on YAML configuration."""
    js_code = []
    
    # Extract stage configuration
    stage_config = data.get('stage', {})
    # Always use 'konva-container' as that's what the web client creates
    container_id = 'konva-container'
    width = stage_config.get('width', 800)
    height = stage_config.get('height', 600)
    
    # Create stage initialization code
    js_code.append("// Create a new Konva stage")
    js_code.append("const stage = new Konva.Stage({")
    js_code.append(f"  container: '{container_id}',")
    js_code.append(f"  width: {width},")
    js_code.append(f"  height: {height}")
    js_code.append("});")
    
    # Process layers
    js_code.append("// Create and add layers")
    layers = data.get('layers', [])
    for i, layer in enumerate(layers):
        layer_name = layer.get('name', f"layer{i}")
        layer_var = f"layer{i}"
        js_code.append(f"// Create layer: {layer_name}")
        js_code.append(f"const {layer_var} = new Konva.Layer();")
        
        # Process objects in the layer
        objects = layer.get('objects', [])
        for j, obj in enumerate(objects):
            obj_type = obj.get('type')
            obj_var = f"obj{i}_{j}"
            
            # Create object with attributes
            attrs = obj.get('attrs', {})
            attrs_json = json.dumps(attrs)
            js_code.append(f"const {obj_var} = new Konva.{obj_type}({attrs_json});")
            
            # Add event listeners if specified
            listeners = obj.get('x-konva-listeners', {})
            for event, handler in listeners.items():
                js_code.append(f"{obj_var}.on('{event}', {handler});")
            
            # Add filters if specified
            filters = obj.get('x-konva-filters', [])
            for filter_name in filters:
                js_code.append(f"{obj_var}.filters([Konva.Filters.{filter_name}]);")
            
            # Set cache option if specified
            if 'x-konva-cache' in obj and obj['x-konva-cache']:
                js_code.append(f"{obj_var}.cache();")
            
            # Add object to layer
            js_code.append(f"{layer_var}.add({obj_var});")
        
        # Add layer to stage
        js_code.append("// Add layer to stage")
        js_code.append(f"stage.add({layer_var});")
    
    # Draw the stage
    js_code.append("// Draw the stage")
    js_code.append("stage.draw();")
    
    # Log to console for debugging
    js_code.append("console.log('Konva stage created with ' + stage.getLayers().length + ' layers');")
    
    return "\n".join(js_code)

@app.get("/health")
async def health_check():
    """Health check endpoint to verify the service is running."""
    return {"status": "healthy"}
