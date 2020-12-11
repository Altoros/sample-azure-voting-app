import os
import tempfile

import pytest
from flask_api import status

from main import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


def test_health(app, client):
    """Health call should return successful status code"""
    rv = client.get('/health')
    assert status.is_success(rv.status_code)

