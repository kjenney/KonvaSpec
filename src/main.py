from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
import yaml

app = FastAPI()

@app.post("/canvas")
async def create_canvas(request: Request):
    yaml_body = await request.body()
    try:
        data = yaml.safe_load(yaml_body)
        # Simulate conversion to JS (actual logic omitted for brevity)
        return {"jsCode": f"// JS output for: {data}"}
    except yaml.YAMLError as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

# Optional: override OpenAPI schema
@app.get("/openapi.json", include_in_schema=False)
async def custom_openapi():
    return get_openapi(
        title="KonvaJS Canvas API",
        version="konva/v9.2.0",
        routes=app.routes,
    )
