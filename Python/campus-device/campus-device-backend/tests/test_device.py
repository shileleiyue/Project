import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from tests.conftest import register_and_login, create_device


# ---------------------------------------------------------------------------
# List devices
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_devices_empty():
    """List devices when none have been created."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        token = await register_and_login(
            client, "dev_list", "13810000001", "pass123", "student"
        )
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/api/devices?page=1&page_size=10", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "list" in data["data"]
        assert "total" in data["data"]


@pytest.mark.asyncio
async def test_get_devices_with_data():
    """List devices after creating some."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "dev_admin1", "13810000002", "admin123", "admin"
        )
        await create_device(client, admin_token, "Device Alpha", "laptop")
        await create_device(client, admin_token, "Device Beta", "projector")

        student_token = await register_and_login(
            client, "dev_student1", "13810000003", "pass123", "student"
        )
        headers = {"Authorization": f"Bearer {student_token}"}
        response = await client.get("/api/devices?page=1&page_size=10", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert len(data["data"]["list"]) >= 2


@pytest.mark.asyncio
async def test_get_devices_unauthorized():
    """Access devices without authentication."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/devices")
        assert response.status_code == 403


# ---------------------------------------------------------------------------
# Get single device
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_device_by_id():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "dev_by_id_admin", "13810000010", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "Device Gamma", "printer")

        student_token = await register_and_login(
            client, "dev_by_id_stu", "13810000011", "pass123", "student"
        )
        headers = {"Authorization": f"Bearer {student_token}"}
        response = await client.get(f"/api/devices/{device_id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["name"] == "Device Gamma"
        assert data["data"]["type"] == "printer"


@pytest.mark.asyncio
async def test_get_device_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        token = await register_and_login(
            client, "dev_404", "13810000012", "pass123", "student"
        )
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/api/devices/99999", headers=headers)
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# Create device (admin only)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_create_device_as_admin():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "create_dev_admin", "13810000020", "admin123", "admin"
        )
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.post("/api/devices", json={
            "name": "New Laptop",
            "type": "laptop",
            "description": "A test laptop",
            "location": "Room 101"
        }, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["msg"] == "设备创建成功"
        assert data["data"]["name"] == "New Laptop"
        assert data["data"]["status"] == "available"


@pytest.mark.asyncio
async def test_create_device_as_student_forbidden():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        token = await register_and_login(
            client, "student_create_dev", "13810000021", "pass123", "student"
        )
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.post("/api/devices", json={
            "name": "Forbidden Device",
            "type": "laptop"
        }, headers=headers)
        assert response.status_code == 403


# ---------------------------------------------------------------------------
# Update device
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_update_device():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "update_dev_admin", "13810000030", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "Old Name", "tablet")

        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.put(f"/api/devices/{device_id}", json={
            "name": "Updated Name",
            "location": "Room 202"
        }, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["name"] == "Updated Name"
        assert data["data"]["location"] == "Room 202"


@pytest.mark.asyncio
async def test_update_device_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "update_404_admin", "13810000031", "admin123", "admin"
        )
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.put("/api/devices/99999", json={
            "name": "Ghost"
        }, headers=headers)
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# Offline device
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_offline_device():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "offline_admin", "13810000040", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "To Offline", "camera")

        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.put(
            f"/api/devices/{device_id}/offline", headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["msg"] == "设备已下架"


# ---------------------------------------------------------------------------
# Delete device
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_delete_device():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "delete_admin", "13810000050", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "To Delete", "monitor")

        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.delete(f"/api/devices/{device_id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["msg"] == "设备已删除"

        # Verify it's gone
        get_resp = await client.get(f"/api/devices/{device_id}", headers=headers)
        assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_device_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "delete_404_admin", "13810000051", "admin123", "admin"
        )
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.delete("/api/devices/99999", headers=headers)
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# Filter devices
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_filter_devices_by_type():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "filter_type_admin", "13810000060", "admin123", "admin"
        )
        await create_device(client, admin_token, "Laptop A", "laptop")
        await create_device(client, admin_token, "Laptop B", "laptop")
        await create_device(client, admin_token, "Projector X", "projector")

        student_token = await register_and_login(
            client, "filter_type_stu", "13810000061", "pass123", "student"
        )
        headers = {"Authorization": f"Bearer {student_token}"}

        response = await client.get(
            "/api/devices?type=laptop", headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        for device in data["data"]["list"]:
            assert device["type"] == "laptop"


@pytest.mark.asyncio
async def test_filter_devices_by_status():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "filter_status_admin", "13810000070", "admin123", "admin"
        )
        await create_device(client, admin_token, "Available Device", "tablet")

        student_token = await register_and_login(
            client, "filter_status_stu", "13810000071", "pass123", "student"
        )
        headers = {"Authorization": f"Bearer {student_token}"}

        response = await client.get(
            "/api/devices?status=available", headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        for device in data["data"]["list"]:
            assert device["status"] == "available"


@pytest.mark.asyncio
async def test_filter_devices_by_keyword():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "filter_kw_admin", "13810000080", "admin123", "admin"
        )
        await create_device(client, admin_token, "UniqueName", "camera")

        student_token = await register_and_login(
            client, "filter_kw_stu", "13810000081", "pass123", "student"
        )
        headers = {"Authorization": f"Bearer {student_token}"}

        response = await client.get(
            "/api/devices?keyword=UniqueName", headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert len(data["data"]["list"]) >= 1
        assert data["data"]["list"][0]["name"] == "UniqueName"


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_devices_pagination():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "page_admin", "13810000090", "admin123", "admin"
        )
        for i in range(5):
            await create_device(client, admin_token, f"Paged Device {i}", "misc")

        student_token = await register_and_login(
            client, "page_stu", "13810000091", "pass123", "student"
        )
        headers = {"Authorization": f"Bearer {student_token}"}

        response = await client.get(
            "/api/devices?page=1&page_size=2", headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert len(data["data"]["list"]) <= 2
        assert data["data"]["page"] == 1
        assert data["data"]["page_size"] == 2