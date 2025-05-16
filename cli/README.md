# Konva CLI Tool

A command-line interface for interacting with the Konva API using YAML configurations.

## Installation

Make sure you have the required dependencies installed:

```bash
pip install click requests pyyaml
```

## Usage

Make the CLI script executable:

```bash
chmod +x konva_cli.py
```

### Commands

#### Create a new canvas

```bash
./konva_cli.py create path/to/konva.yaml
```

#### Get a canvas by ID

```bash
./konva_cli.py get <canvas_id>
```

#### Update an existing canvas

```bash
./konva_cli.py update <canvas_id> path/to/updated_konva.yaml
```

#### Delete a canvas

```bash
./konva_cli.py delete <canvas_id>
```

#### List all canvases

```bash
./konva_cli.py list
```

#### Generate JavaScript code from YAML

```bash
./konva_cli.py generate-js path/to/konva.yaml
```

Save the generated JavaScript to a file:

```bash
./konva_cli.py generate-js path/to/konva.yaml --output output.js
```

### Options

- `--api-url`: Specify a custom API URL (default: http://localhost:8000)

Example:
```bash
./konva_cli.py --api-url http://api.example.com create path/to/konva.yaml
```

## Example YAML Format

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
