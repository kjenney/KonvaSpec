#!/usr/bin/env python3
import os
import sys
import yaml
import json
import click
import requests
from typing import Optional, Dict, Any

# Default API URL
DEFAULT_API_URL = "http://localhost:8000"

class KonvaAPI:
    """Client for interacting with the Konva API."""
    
    def __init__(self, api_url: str = DEFAULT_API_URL):
        self.api_url = api_url
    
    def create_canvas(self, yaml_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new canvas configuration."""
        response = requests.post(
            f"{self.api_url}/canvas",
            data=yaml.dump(yaml_data),
            headers={"Content-Type": "application/yaml"}
        )
        response.raise_for_status()
        return response.json()
    
    def get_canvas(self, canvas_id: str) -> Dict[str, Any]:
        """Get a canvas configuration by ID."""
        response = requests.get(f"{self.api_url}/canvas/{canvas_id}")
        response.raise_for_status()
        return response.json()
    
    def update_canvas(self, canvas_id: str, yaml_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing canvas configuration."""
        response = requests.put(
            f"{self.api_url}/canvas/{canvas_id}",
            data=yaml.dump(yaml_data),
            headers={"Content-Type": "application/yaml"}
        )
        response.raise_for_status()
        return response.json()
    
    def delete_canvas(self, canvas_id: str) -> Dict[str, Any]:
        """Delete a canvas configuration."""
        response = requests.delete(f"{self.api_url}/canvas/{canvas_id}")
        response.raise_for_status()
        return response.json()
    
    def list_canvases(self) -> Dict[str, Any]:
        """List all canvas configurations."""
        response = requests.get(f"{self.api_url}/canvas")
        response.raise_for_status()
        return response.json()


@click.group()
@click.option('--api-url', default=DEFAULT_API_URL, help='URL of the Konva API.')
@click.pass_context
def cli(ctx, api_url):
    """CLI tool for interacting with the Konva API using YAML configurations."""
    ctx.ensure_object(dict)
    ctx.obj['api'] = KonvaAPI(api_url)


@cli.command()
@click.argument('yaml_file', type=click.Path(exists=True))
@click.pass_context
def create(ctx, yaml_file):
    """Create a new canvas from a YAML file."""
    try:
        with open(yaml_file, 'r') as f:
            yaml_data = yaml.safe_load(f)
        
        result = ctx.obj['api'].create_canvas(yaml_data)
        click.echo(f"Canvas created successfully: {json.dumps(result, indent=2)}")
    except Exception as e:
        click.echo(f"Error creating canvas: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('canvas_id')
@click.pass_context
def get(ctx, canvas_id):
    """Get a canvas configuration by ID."""
    try:
        result = ctx.obj['api'].get_canvas(canvas_id)
        click.echo(yaml.dump(result, default_flow_style=False))
    except Exception as e:
        click.echo(f"Error retrieving canvas: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('canvas_id')
@click.argument('yaml_file', type=click.Path(exists=True))
@click.pass_context
def update(ctx, canvas_id, yaml_file):
    """Update an existing canvas configuration."""
    try:
        with open(yaml_file, 'r') as f:
            yaml_data = yaml.safe_load(f)
        
        result = ctx.obj['api'].update_canvas(canvas_id, yaml_data)
        click.echo(f"Canvas updated successfully: {json.dumps(result, indent=2)}")
    except Exception as e:
        click.echo(f"Error updating canvas: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('canvas_id')
@click.pass_context
def delete(ctx, canvas_id):
    """Delete a canvas configuration."""
    try:
        result = ctx.obj['api'].delete_canvas(canvas_id)
        click.echo(f"Canvas deleted successfully: {json.dumps(result, indent=2)}")
    except Exception as e:
        click.echo(f"Error deleting canvas: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def list(ctx):
    """List all canvas configurations."""
    try:
        result = ctx.obj['api'].list_canvases()
        click.echo(yaml.dump(result, default_flow_style=False))
    except Exception as e:
        click.echo(f"Error listing canvases: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('yaml_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file for the generated JS code.')
@click.pass_context
def generate_js(ctx, yaml_file, output):
    """Generate JavaScript code from a YAML configuration."""
    try:
        with open(yaml_file, 'r') as f:
            yaml_data = yaml.safe_load(f)
        
        result = ctx.obj['api'].create_canvas(yaml_data)
        js_code = result.get('jsCode', '')
        
        if output:
            with open(output, 'w') as f:
                f.write(js_code)
            click.echo(f"JavaScript code written to {output}")
        else:
            click.echo(js_code)
    except Exception as e:
        click.echo(f"Error generating JavaScript: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli(obj={})
