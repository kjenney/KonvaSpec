import pytest
import json
import yaml
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from cli.konva_cli import cli, KonvaAPI

@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()

@pytest.fixture
def mock_api():
    """Create a mock KonvaAPI instance."""
    with patch('cli.konva_cli.KonvaAPI') as mock:
        api_instance = MagicMock()
        mock.return_value = api_instance
        yield api_instance

def test_create_command(runner, mock_api, tmp_path):
    """Test the create command."""
    # Create a test YAML file
    test_data = {"type": "rect", "width": 100, "height": 50}
    yaml_file = tmp_path / "test.yaml"
    with open(yaml_file, 'w') as f:
        yaml.dump(test_data, f)
    
    # Mock the API response
    mock_api.create_canvas.return_value = {
        "id": "test-id",
        "jsCode": "// JS code",
        "data": test_data
    }
    
    # Run the command
    result = runner.invoke(cli, ['create', str(yaml_file)])
    
    # Check the results
    assert result.exit_code == 0
    assert "Canvas created successfully" in result.output
    mock_api.create_canvas.assert_called_once_with(test_data)

def test_get_command(runner, mock_api):
    """Test the get command."""
    # Mock the API response
    test_data = {"type": "rect", "width": 100, "height": 50}
    mock_api.get_canvas.return_value = {
        "id": "test-id",
        "data": test_data
    }
    
    # Run the command
    result = runner.invoke(cli, ['get', 'test-id'])
    
    # Check the results
    assert result.exit_code == 0
    mock_api.get_canvas.assert_called_once_with('test-id')
    # Verify YAML output contains the data
    assert "type: rect" in result.output
    assert "width: 100" in result.output
    assert "height: 50" in result.output

def test_update_command(runner, mock_api, tmp_path):
    """Test the update command."""
    # Create a test YAML file
    test_data = {"type": "rect", "width": 200, "height": 75}
    yaml_file = tmp_path / "update.yaml"
    with open(yaml_file, 'w') as f:
        yaml.dump(test_data, f)
    
    # Mock the API response
    mock_api.update_canvas.return_value = {
        "id": "test-id",
        "jsCode": "// Updated JS code",
        "data": test_data
    }
    
    # Run the command
    result = runner.invoke(cli, ['update', 'test-id', str(yaml_file)])
    
    # Check the results
    assert result.exit_code == 0
    assert "Canvas updated successfully" in result.output
    mock_api.update_canvas.assert_called_once_with('test-id', test_data)

def test_delete_command(runner, mock_api):
    """Test the delete command."""
    # Mock the API response
    test_data = {"type": "rect", "width": 100, "height": 50}
    mock_api.delete_canvas.return_value = {
        "id": "test-id",
        "message": "Canvas deleted successfully",
        "data": test_data
    }
    
    # Run the command
    result = runner.invoke(cli, ['delete', 'test-id'])
    
    # Check the results
    assert result.exit_code == 0
    assert "Canvas deleted successfully" in result.output
    mock_api.delete_canvas.assert_called_once_with('test-id')

def test_list_command(runner, mock_api):
    """Test the list command."""
    # Mock the API response
    test_data = [
        {"id": "id1", "data": {"type": "rect"}},
        {"id": "id2", "data": {"type": "circle"}}
    ]
    mock_api.list_canvases.return_value = test_data
    
    # Run the command
    result = runner.invoke(cli, ['list'])
    
    # Check the results
    assert result.exit_code == 0
    mock_api.list_canvases.assert_called_once()
    # Verify YAML output contains the data
    assert "id: id1" in result.output
    assert "type: rect" in result.output
    assert "id: id2" in result.output
    assert "type: circle" in result.output

def test_generate_js_command(runner, mock_api, tmp_path):
    """Test the generate-js command."""
    # Create a test YAML file
    test_data = {"type": "rect", "width": 100, "height": 50}
    yaml_file = tmp_path / "test.yaml"
    with open(yaml_file, 'w') as f:
        yaml.dump(test_data, f)
    
    # Mock the API response
    mock_api.create_canvas.return_value = {
        "id": "test-id",
        "jsCode": "// Generated JS code",
        "data": test_data
    }
    
    # Test without output file
    result = runner.invoke(cli, ['generate-js', str(yaml_file)])
    assert result.exit_code == 0
    assert "// Generated JS code" in result.output
    
    # Test with output file
    output_file = tmp_path / "output.js"
    result = runner.invoke(cli, ['generate-js', str(yaml_file), '--output', str(output_file)])
    assert result.exit_code == 0
    assert f"JavaScript code written to {output_file}" in result.output
    with open(output_file, 'r') as f:
        assert f.read() == "// Generated JS code"

def test_api_error_handling(runner, mock_api, tmp_path):
    """Test error handling in CLI commands."""
    # Create a test YAML file
    test_data = {"type": "rect", "width": 100, "height": 50}
    yaml_file = tmp_path / "test.yaml"
    with open(yaml_file, 'w') as f:
        yaml.dump(test_data, f)
    
    # Mock API to raise an exception
    mock_api.create_canvas.side_effect = Exception("API error")
    
    # Run the command
    result = runner.invoke(cli, ['create', str(yaml_file)])
    
    # Check the results
    assert result.exit_code == 1
    assert "Error creating canvas: API error" in result.output
