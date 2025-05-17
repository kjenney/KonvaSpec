# API Usage Guide

This guide provides detailed information on how to use the KonvaJS Canvas API.

## Overview

The KonvaJS Canvas API allows you to define KonvaJS scenes and components using YAML. This API supports the full canvas hierarchy, animations, transitions, events, caching, filters, and more.

## API Endpoints

<div class="api-endpoint">
<strong>POST</strong> <code>/canvas</code>

Create a new canvas with KonvaJS objects
</div>

## Request Format

The API accepts YAML definitions of KonvaJS objects. Here's an example of a valid request body:

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

## Response Format

The API returns JavaScript code that can be used to render the KonvaJS objects in a web application.

## Authentication

Currently, the API does not require authentication for requests.

## Rate Limiting

There are no rate limits currently implemented for the API.

## Error Handling

The API returns standard HTTP status codes to indicate the success or failure of a request:

- `200 OK`: The request was successful
- `400 Bad Request`: The request was invalid or could not be understood
- `500 Internal Server Error`: An error occurred on the server

## Examples

### Basic Example

Here's a basic example of how to use the API with the Python client:

```python
from konva_client import KonvaClient

# Initialize the client
client = KonvaClient()

# Send the YAML file to the server
response = client.render_canvas("examples/konva.yaml")

# Print the response
print(response)
```

### Advanced Example

For more advanced usage, you can define complex KonvaJS scenes with animations, transitions, and event handlers:

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
          click: "function(evt) { this.to({ fill: 'red', duration: 0.5 }); }"
          mouseover: "function(evt) { document.body.style.cursor = 'pointer'; }"
          mouseout: "function(evt) { document.body.style.cursor = 'default'; }"
        x-konva-animation:
          duration: 2
          easing: 'EaseInOut'
          properties:
            x: 300
            rotation: 360
```

## Further Resources

For more information on KonvaJS, visit the [official KonvaJS documentation](https://konvajs.org/docs/).
