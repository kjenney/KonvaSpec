# KonvaSpec

An OpenAPI-compliant, versioned YAML-based API for defining and rendering KonvaJS objects.

## Usage

### Server

```bash
docker compose up
```

### Client

```python
from konva_client import KonvaClient

client = KonvaClient()
response = client.render_canvas("path/to/your/file.yaml")
print(response)
```

