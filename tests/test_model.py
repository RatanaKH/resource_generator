import os
import shutil

import pytest
from typer.testing import CliRunner

from resource_generator.main import app

runner = CliRunner()

TEMP_DIR = "app/models"

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
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)


def test_make_model(setup_data):
    result = runner.invoke(app, ["make-model", "name", "Users"])
    assert result.exit_code == 0, f"Unexpected exit code: {result.exit_code}"
    assert "A Models Users created successfully!" in result.stdout

def test_make_model_and_already_exist(setup_data):
    runner.invoke(app, ["make-model", "name", "Users"])
    result = runner.invoke(app, ["make-model", "name", "Users"])
    assert result.exit_code == 0
    assert "already exists!" in result.stdout , f"Unexpected error message: {result.stdout}"

def test_auto_make_base_model(setup_data):
    result = runner.invoke(app, ["make-model", "name", "Users"])
    assert os.path.exists(TEMP_DIR + "/base_model.py") == True
    assert "A Models Base created successfully!" in result.stdout

def test_auto_make_base_model_already_exist():
    runner.invoke(app, ["make-model", "name", "Users"])
    result = runner.invoke(app, ["make-model", "name", "Users123"])
    assert os.path.exists(TEMP_DIR + "/base_model.py") == True
    assert "A Models Base created successfully!" not in result.stdout

def test_make_model_with_controller_option():
    result = runner.invoke(app, ["make-model", "name", "Users", "--controller"])
    assert "A Controllers Users created successfully!" in result.stdout

def test_make_model_with_service_option():
    result = runner.invoke(app, ["make-model", "name", "Users", "--service"])
    assert "A Services Users created successfully!" in result.stdout

def test_make_model_with_schema_option():
    result = runner.invoke(app, ["make-model", "name", "Users", "--schema"])
    assert "A Schema Users created successfully!" in result.stdout

def test_make_model_with_repository_option():
    result = runner.invoke(app, ["make-model", "name", "Users", "--repository"])
    assert "A Repository Users created successfully!" in result.stdout

