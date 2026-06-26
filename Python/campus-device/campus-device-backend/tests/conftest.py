"""
Test configuration for campus-device-backend.

Overrides the database URL to use SQLite for testing so no MySQL server is needed.
"""
import os
import sys

# ---------------------------------------------------------------------------
# MUST set DATABASE_URL before any app-code imports.
# The settings class reads env vars at import time, and models/__init__.py
# creates the async engine at module level.
# ---------------------------------------------------------------------------
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

# Now it is safe to import the app and models.
from app.main import app
from app.models import Base, engine


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    """Create all tables before the test session, drop them after."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
    # Remove the SQLite file
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test.db")
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest_asyncio.fixture
async def client():
    """Async HTTP test client that talks directly to the FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# ---------------------------------------------------------------------------
# Helper functions used by test modules
# ---------------------------------------------------------------------------

async def register_and_login(client, username, phone, password, role="student"):
    """Register a user and return the auth token."""
    # Register (ignore 409 if already registered by another test)
    await client.post("/api/auth/register", json={
        "username": username,
        "phone": phone,
        "password": password,
        "role": role,
    })
    # Login
    resp = await client.post("/api/auth/login", json={
        "phone": phone,
        "password": password,
    })
    data = resp.json()
    return data["data"]["token"]


async def create_device(client, admin_token, name="Test Device", type="laptop"):
    """Create a device and return its id."""
    resp = await client.post("/api/devices", json={
        "name": name,
        "type": type,
        "description": "Test device for automated tests",
        "location": "Test Lab",
    }, headers={"Authorization": f"Bearer {admin_token}"})
    return resp.json()["data"]["id"]