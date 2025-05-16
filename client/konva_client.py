import requests
import yaml

class KonvaClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def render_canvas(self, yaml_file_path):
        with open(yaml_file_path, 'r') as f:
            yaml_data = f.read()
        headers = {'Content-Type': 'application/yaml'}
        response = requests.post(f"{self.base_url}/canvas", data=yaml_data, headers=headers)
        response.raise_for_status()
        return response.json()
