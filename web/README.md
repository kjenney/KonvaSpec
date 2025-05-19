# KonvaSpec Web Client

This is a web client for testing the KonvaSpec YAML API. It allows you to:

1. Enter YAML configurations in a form
2. Submit the YAML to the API
3. View the generated JavaScript
4. Inject and execute the JavaScript in the page to preview the Konva canvas

## Prerequisites

- Node.js and npm installed
- The main KonvaSpec API server running (typically on port 8000)

## Installation

Install the dependencies:

```bash
npm install
```

## Usage

1. Start the web server:

```bash
npm start
```

2. Open your browser and navigate to http://localhost:3000

3. Enter your YAML configuration in the text area

4. Click "Generate JavaScript" to send the YAML to the API

5. Click "Inject JavaScript" to execute the generated JavaScript and see the preview

## Notes

- The web server runs on port 3000 by default
- The client assumes the main API is running on http://localhost:8000
- CORS is enabled to allow cross-origin requests between the web client and API
