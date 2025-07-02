import pytest
from flask import Flask
from flask.testing import FlaskClient
import json

from flask_app import app  # Import your Flask app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_ask_success(client):
    """
    Tests the /ask endpoint for a successful response (Flask version).
    """
    response = client.post("/ask", json={"question": "What is Flask?", "source": "hf"})
    assert response.status_code == 200
    data = response.get_json()
    assert "answer" in data
    assert "sources" in data
    assert "tokens" in data
    assert data["answer"].startswith("Sample answer for:")
    assert isinstance(data["sources"], list)
    assert isinstance(data["tokens"], int)


def test_ask_llm_success(client):
    """
    Tests the /ask_llm endpoint for a successful response (Flask version).
    """
    response = client.post("/ask_llm", json={"question": "What is an LLM?"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["answer"] == "This is a sample LLM answer."
    assert data["source_url"] == "https://stackoverflow.com/q/123456"