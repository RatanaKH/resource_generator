import os
import shutil

import pytest
from typer.testing import CliRunner

from resource_generator.main import app

runner = CliRunner()

TEMP_DIR = "app/services"
APP_DIR = os.path.dirname(TEMP_DIR)

@pytest.fixture
def setup_data():
    data = TEMP_DIR
    """Setup function to prepare a clean state before each test."""
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR)
    print("\nSetting up resources...")
    yield data  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    print("\nTearing down resources...")
    if os.path.exists(APP_DIR):
        shutil.rmtree(APP_DIR)


def test_make_service(setup_data):
    result = runner.invoke(app, ["make-service", "name", "Users"])
    assert result.exit_code == 0, f"Unexpected exit code: {result.exit_code}"
    assert "A Services Users created successfully!" in result.stdout

def test_make_service_and_already_exist(setup_data):
    runner.invoke(app, ["make-service", "name", "Users"])
    result = runner.invoke(app, ["make-service", "name", "Users"])
    assert result.exit_code == 0
    assert "already exists!" in result.stdout , f"Unexpected error message: {result.stdout}"
