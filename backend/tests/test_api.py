import pytest
from httpx import AsyncClient
from app_main import app
import os
import asyncio

@pytest.mark.anyio
async def test_ask_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/ask", json={"question": "What is FastAPI?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert "tokens" in data

@pytest.mark.anyio
async def test_ask_hf_python():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/ask", json={"question": "How do I use Python lists?", "source": "hf"})
    assert response.status_code == 200
    data = response.json()
    assert "sources" in data
    assert any("python" in s["question"].lower() for s in data["sources"])

@pytest.mark.anyio
async def test_ask_hf_kubernetes():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/ask", json={"question": "What is Kubernetes?", "source": "hf"})
    assert response.status_code == 200
    data = response.json()
    assert "sources" in data
    assert any("kubernetes" in s["question"].lower() for s in data["sources"])

@pytest.mark.anyio
async def test_ask_hf_general():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/ask", json={"question": "What is Kubernetes?", "source": "hf"})
    assert response.status_code == 200
    data = response.json()
    assert "sources" in data
    assert isinstance(data["sources"], list)
    assert len(data["sources"]) > 0
    assert any("kubernetes" in s["question"].lower() for s in data["sources"])
