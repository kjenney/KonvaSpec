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

## Documentation

The project includes API documentation built with MkDocs and Swagger UI.

### Local Development

To run the documentation site locally:

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install documentation dependencies
pip install -r requirements-docs.txt

# Serve the documentation site locally
mkdocs serve
```

This will start a local server at http://127.0.0.1:8000 where you can preview the documentation.

### Documentation Structure

- `docs/index.md`: Main landing page
- `docs/swagger-ui.md`: Interactive API documentation using Swagger UI
- `docs/openapi/konva-v9.2.0.yaml`: OpenAPI specification file

### GitHub Pages Deployment

The documentation is automatically deployed to GitHub Pages when changes are pushed to the main branch. The GitHub workflow in `.github/workflows/docs.yml` handles the build and deployment process.

You can also manually trigger a deployment by running the workflow from the GitHub Actions tab.

## Getting Started

KonvaSpec allows you to define KonvaJS objects in YAML and convert them to JavaScript code that can be used in your web applications. This guide will walk you through the process of using the example konva.yaml file with the Python client to generate JavaScript code.

### Prerequisites

- Python 3.6 or higher
- Docker and Docker Compose (for running the server)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd KonvaSpec
```

### Step 2: Start the Server

The server processes YAML files and converts them to JavaScript code.

```bash
docker compose up
```

This will start the server on http://localhost:8000.

### Step 3: Install the Python Client

```bash
pip install -r requirements.txt
```

### Step 4: Use the Example YAML File

The repository includes an example YAML file at `examples/konva.yaml` that defines a stage with a rectangle and a circle:

```yaml
stage:
  container: 'canvas-container'
  width: 800
  height: 600
layers:
  - name: 'main-layer'
    objects:
      - type: Rect
        attrs:
          x: 50
          y: 60
          width: 200
          height: 100
          fill: 'green'
        x-konva-listeners:
          click: "function(evt) { alert('Rectangle clicked'); }"
      - type: Circle
        attrs:
          x: 400
          y: 300
          radius: 75
          fill: 'blue'
        x-konva-filters:
          - Blur
          - Grayscale
        x-konva-cache: true
```

### Step 5: Generate JavaScript Code

Use the Python client to send the YAML file to the server and get the JavaScript code:

```python
from konva_client import KonvaClient

# Initialize the client
client = KonvaClient()

# Send the YAML file to the server
response = client.render_canvas("examples/konva.yaml")

# Print the response
print(response)

# The response contains the JavaScript code in the 'jsCode' field
js_code = response['jsCode']
print(js_code)
```

### Step 6: Use the Generated JavaScript Code

The generated JavaScript code can be included in your HTML file:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Konva Example</title>
    <script src="https://unpkg.com/konva@9.2.0/konva.min.js"></script>
</head>
<body>
    <div id="canvas-container"></div>
    <script>
        // Paste the generated JavaScript code here
    </script>
</body>
</html>
```