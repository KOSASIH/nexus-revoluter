import os
import pytest
import json
import logging
from utils import setup_logging, AppException, load_config, validate_input, save_to_json, load_from_json

# Test data
TEST_CONFIG_FILE = "test_config.json"
TEST_JSON_FILE = "test_data.json"

# Sample configuration for testing
SAMPLE_CONFIG = {
    "setting1": "value1",
    "setting2": "value2"
}

# Sample data for JSON testing
SAMPLE_DATA = {
    "key1": "value1",
    "key2": "value2"
}

@pytest.fixture(scope="module", autouse=True)
def setup_module():
    """Setup for the entire module."""
    # Create a test config file
    with open(TEST_CONFIG_FILE, 'w') as f:
        json.dump(SAMPLE_CONFIG, f)

    # Create a test JSON file
    with open(TEST_JSON_FILE, 'w') as f:
        json.dump(SAMPLE_DATA, f)

    # Setup logging
    setup_logging()

def test_load_config():
    """Test loading configuration from a JSON file."""
    config = load_config(TEST_CONFIG_FILE)
    assert config == SAMPLE_CONFIG

def test_load_config_file_not_found():
    """Test loading configuration from a non-existent file."""
    with pytest.raises(AppException) as excinfo:
        load_config("non_existent_config.json")
    assert excinfo.value.status_code == 404
    assert "Configuration file" in str(excinfo.value)

def test_validate_input_success():
    """Test successful input validation."""
    data = {"key1": "value1", "key2": "value2"}
    validate_input(data, ["key1", "key2"])  # Should not raise an exception

def test_validate_input_missing_field():
    """Test input validation for missing required fields."""
    data = {"key1": "value1"}
    with pytest.raises(AppException) as excinfo:
        validate_input(data, ["key1", "key2"])
    assert excinfo.value.status_code == 400
    assert "Missing required field" in str(excinfo.value)

def test_validate_input_empty_field():
    """Test input validation for empty fields."""
    data = {"key1": "", "key2": "value2"}
    with pytest.raises(AppException) as excinfo:
        validate_input(data, ["key1", "key2"])
    assert excinfo.value.status_code == 400
    assert "Field 'key1' cannot be empty." in str(excinfo.value)

def test_save_to_json():
    """Test saving data to a JSON file."""
    save_to_json(SAMPLE_DATA, TEST_JSON_FILE)
    with open(TEST_JSON_FILE, 'r') as f:
        data = json.load(f)
    assert data == SAMPLE_DATA

def test_load_from_json():
    """Test loading data from a JSON file."""
    data = load_from_json(TEST_JSON_FILE)
    assert data == SAMPLE_DATA

def test_load_from_json_file_not_found():
    """Test loading data from a non-existent JSON file."""
    with pytest.raises(AppException) as excinfo:
        load_from_json("non_existent_file.json")
    assert excinfo.value.status_code == 404
    assert "File 'non_existent_file.json' not found." in str(excinfo.value)

def teardown_module(module):
    """Teardown for the entire module."""
    if os.path.exists(TEST_CONFIG_FILE):
        os.remove(TEST_CONFIG_FILE)
    if os.path.exists(TEST_JSON_FILE):
        os.remove(TEST_JSON_FILE)

if __name__ == "__main__":
    pytest.main()
