import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from tests.conftest import register_and_login


# ---------------------------------------------------------------------------
# Registration tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_register_student():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/auth/register", json={
            "username": "test_student",
            "phone": "13800000001",
            "password": "123456",
            "role": "student"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["msg"] == "注册成功"
        assert data["data"]["username"] == "test_student"


@pytest.mark.asyncio
async def test_register_admin():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/auth/register", json={
            "username": "test_admin",
            "phone": "13800000002",
            "password": "admin123",
            "role": "admin"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200


@pytest.mark.asyncio
async def test_register_repairer():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/auth/register", json={
            "username": "test_repairer",
            "phone": "13800000003",
            "password": "repair123",
            "role": "repairer"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200


@pytest.mark.asyncio
async def test_register_duplicate_phone():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # First registration
        await client.post("/api/auth/register", json={
            "username": "dup_phone_a",
            "phone": "13800000010",
            "password": "123456",
            "role": "student"
        })
        # Duplicate phone with different username
        response = await client.post("/api/auth/register", json={
            "username": "dup_phone_b",
            "phone": "13800000010",
            "password": "123456",
            "role": "student"
        })
        assert response.status_code == 409
        data = response.json()
        assert "手机号" in data.get("detail", "")


@pytest.mark.asyncio
async def test_register_duplicate_username():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # First registration
        await client.post("/api/auth/register", json={
            "username": "dup_username",
            "phone": "13800000011",
            "password": "123456",
            "role": "student"
        })
        # Duplicate username with different phone
        response = await client.post("/api/auth/register", json={
            "username": "dup_username",
            "phone": "13800000012",
            "password": "123456",
            "role": "student"
        })
        assert response.status_code == 409
        data = response.json()
        assert "用户名" in data.get("detail", "")


@pytest.mark.asyncio
async def test_register_invalid_role():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/auth/register", json={
            "username": "invalid_role_user",
            "phone": "13800000013",
            "password": "123456",
            "role": "superadmin"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        # Should default to student
        login_resp = await client.post("/api/auth/login", json={
            "phone": "13800000013",
            "password": "123456"
        })
        # Verify the role is student by checking what token can access
        token = login_resp.json()["data"]["token"]
        # Try to access admin-only endpoint - should get 403
        admin_resp = await client.get("/api/borrows", headers={
            "Authorization": f"Bearer {token}"
        })
        assert admin_resp.status_code == 403


# ---------------------------------------------------------------------------
# Login tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_login_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        token = await register_and_login(
            client, "login_test", "13800000020", "pass123", "student"
        )
        assert token is not None


@pytest.mark.asyncio
async def test_login_wrong_password():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register first
        await client.post("/api/auth/register", json={
            "username": "wrong_pwd_user",
            "phone": "13800000021",
            "password": "correct",
            "role": "student"
        })
        # Try wrong password
        response = await client.post("/api/auth/login", json={
            "phone": "13800000021",
            "password": "wrong"
        })
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/auth/login", json={
            "phone": "13999999999",
            "password": "whatever"
        })
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_wrong_phone():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/auth/register", json={
            "username": "wrong_phone_user",
            "phone": "13800000022",
            "password": "pass123",
            "role": "student"
        })
        response = await client.post("/api/auth/login", json={
            "phone": "13800000023",  # different phone
            "password": "pass123"
        })
        assert response.status_code == 401


# ---------------------------------------------------------------------------
# Logout test
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_logout():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        token = await register_and_login(
            client, "logout_user", "13800000030", "pass123", "student"
        )
        response = await client.post("/api/auth/logout", headers={
            "Authorization": f"Bearer {token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200


# ---------------------------------------------------------------------------
# Get current user (/me) tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_me():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        token = await register_and_login(
            client, "me_user", "13800000040", "pass123", "student"
        )
        response = await client.get("/api/auth/me", headers={
            "Authorization": f"Bearer {token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["username"] == "me_user"
        assert data["data"]["phone"] == "13800000040"


@pytest.mark.asyncio
async def test_get_me_unauthorized():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/auth/me")
        assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_me_invalid_token():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/auth/me", headers={
            "Authorization": "Bearer invalid_token_here"
        })
        assert response.status_code == 401