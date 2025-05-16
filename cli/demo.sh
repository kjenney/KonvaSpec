#!/bin/bash
# Demo script for Konva CLI tool

# Set variables
EXAMPLE_YAML="/Users/kjenney/devel/sprite-cinema/KonvaSpec/examples/konva.yaml"
CLI_TOOL="/Users/kjenney/devel/sprite-cinema/KonvaSpec/cli/konva_cli.py"

# Start the FastAPI server in the background
echo "Starting the FastAPI server..."
cd /Users/kjenney/devel/sprite-cinema/KonvaSpec
python -m uvicorn src.main:app --reload &
SERVER_PID=$!

# Wait for the server to start
echo "Waiting for server to start..."
sleep 3

# Create a new canvas
echo -e "\n1. Creating a new canvas from YAML file..."
RESPONSE=$($CLI_TOOL create $EXAMPLE_YAML)
echo "$RESPONSE"

# Extract the canvas ID from the response
CANVAS_ID=$(echo "$RESPONSE" | grep -o '"id": "[^"]*' | cut -d'"' -f4)
echo "Canvas ID: $CANVAS_ID"

# List all canvases
echo -e "\n2. Listing all canvases..."
$CLI_TOOL list

# Get a specific canvas
echo -e "\n3. Getting canvas with ID: $CANVAS_ID..."
$CLI_TOOL get $CANVAS_ID

# Update the canvas
echo -e "\n4. Updating the canvas..."
$CLI_TOOL update $CANVAS_ID $EXAMPLE_YAML

# Generate JavaScript code
echo -e "\n5. Generating JavaScript code..."
$CLI_TOOL generate-js $EXAMPLE_YAML

# Delete the canvas
echo -e "\n6. Deleting the canvas..."
$CLI_TOOL delete $CANVAS_ID

# List all canvases again to confirm deletion
echo -e "\n7. Listing all canvases after deletion..."
$CLI_TOOL list

# Clean up - kill the server
echo -e "\nStopping the FastAPI server..."
kill $SERVER_PID

echo -e "\nDemo completed!"
