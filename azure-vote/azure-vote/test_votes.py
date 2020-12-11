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

def test(app, client):
    assert True

