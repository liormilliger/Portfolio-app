import pytest
from main import app  # Import your Flask app
from flask_pymongo import PyMongo
from mongomock import MongoClient
import mongomock

# Setup the Flask test client
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Mock MongoDB
@pytest.fixture
def mock_mongo(monkeypatch):
    mock_db = mongomock.MongoClient().db
    monkeypatch.setattr(PyMongo, 'db', mock_db)
    return mock_db

# Example test: Ensure the homepage loads
def test_homepage_status(client):
    response = client.get('/')  # Replace '/' with the actual route
    assert response.status_code == 200

# Example test: Check content in homepage
def test_homepage_content(client):
    response = client.get('/')  # Replace '/' with the actual route
    assert 'Welcome' in response.get_data(as_text=True)  # Replace 'Welcome' with expected text

# Example test: Interacting with the mocked database
def test_database_interaction(mock_mongo):
    # Use mock_mongo to perform database operations
    # Example: mock_mongo.collection.insert_one({"key": "value"})
    # Perform your test assertions here
