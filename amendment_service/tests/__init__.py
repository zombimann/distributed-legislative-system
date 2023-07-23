# tests/__init__.py
import pytest

from app import app, db

@pytest.fixture
def client():
    app.config.from_object('config.TestConfig')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

