import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from tests.conftest import register_and_login, create_device


# ---------------------------------------------------------------------------
# Create repair
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_create_repair():
    """Admin creates a repair order for a device."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "repair_admin", "13830000001", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "Repair Device", "laptop")

        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.post("/api/repairs", json={
            "device_id": device_id,
            "fault_description": "Won't boot up"
        }, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["device_id"] == device_id
        assert data["data"]["status"] == "pending"


@pytest.mark.asyncio
async def test_create_repair_nonexistent_device():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "repair_404_admin", "13830000002", "admin123", "admin"
        )
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.post("/api/repairs", json={
            "device_id": 99999,
            "fault_description": "Ghost device"
        }, headers=headers)
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_repair_as_student_forbidden():
    """Students cannot create repair orders."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        student_token = await register_and_login(
            client, "repair_stu", "13830000003", "pass123", "student"
        )
        headers = {"Authorization": f"Bearer {student_token}"}
        response = await client.post("/api/repairs", json={
            "device_id": 1,
            "fault_description": "Test"
        }, headers=headers)
        assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_repair_unauthorized():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/repairs", json={
            "device_id": 1,
            "fault_description": "Test"
        })
        assert response.status_code == 403


# ---------------------------------------------------------------------------
# Get repairs
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_repairs_as_admin():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "list_repair_admin", "13830000010", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "List Repair Device", "laptop")

        headers = {"Authorization": f"Bearer {admin_token}"}
        await client.post("/api/repairs", json={
            "device_id": device_id,
            "fault_description": "Test"
        }, headers=headers)

        response = await client.get("/api/repairs", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "list" in data["data"]


@pytest.mark.asyncio
async def test_get_my_repairs():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "my_repair_admin", "13830000020", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "My Repair Device", "laptop")

        headers = {"Authorization": f"Bearer {admin_token}"}
        await client.post("/api/repairs", json={
            "device_id": device_id,
            "fault_description": "My repair"
        }, headers=headers)

        response = await client.get("/api/repairs/my", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert len(data["data"]["list"]) >= 1


# ---------------------------------------------------------------------------
# Get repair by id
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_repair_by_id():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "get_repair_admin", "13830000030", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "Get Repair Device", "laptop")

        headers = {"Authorization": f"Bearer {admin_token}"}
        resp = await client.post("/api/repairs", json={
            "device_id": device_id,
            "fault_description": "Detail test"
        }, headers=headers)
        repair_id = resp.json()["data"]["id"]

        response = await client.get(f"/api/repairs/{repair_id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["id"] == repair_id


@pytest.mark.asyncio
async def test_get_repair_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "repair_404b_admin", "13830000031", "admin123", "admin"
        )
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.get("/api/repairs/99999", headers=headers)
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# Assign repairer
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_assign_repair():
    """Admin assigns a repairer to a repair order."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "assign_admin", "13830000040", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "Assign Device", "laptop")

        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        # Create repair
        resp = await client.post("/api/repairs", json={
            "device_id": device_id,
            "fault_description": "Assign test"
        }, headers=admin_headers)
        repair_id = resp.json()["data"]["id"]

        # Register a repairer
        repairer_token = await register_and_login(
            client, "assign_repairer", "13830000041", "repair123", "repairer"
        )
        repairer_headers = {"Authorization": f"Bearer {repairer_token}"}
        # Get the repairer's user id from /me
        me_resp = await client.get("/api/auth/me", headers=repairer_headers)
        repairer_id = me_resp.json()["data"]["id"]

        # Admin assigns the repairer
        response = await client.put(
            f"/api/repairs/{repair_id}/assign",
            json={"assigned_to": repairer_id}, headers=admin_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["assigned_to"] == repairer_id


# ---------------------------------------------------------------------------
# Update repair status (repairer)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_update_repair_status():
    """Repairer updates the repair status."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "status_admin", "13830000050", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "Status Device", "laptop")
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        # Create repair
        resp = await client.post("/api/repairs", json={
            "device_id": device_id,
            "fault_description": "Status test"
        }, headers=admin_headers)
        repair_id = resp.json()["data"]["id"]

        # Register repairer and assign
        repairer_token = await register_and_login(
            client, "status_repairer", "13830000051", "repair123", "repairer"
        )
        repairer_headers = {"Authorization": f"Bearer {repairer_token}"}
        me_resp = await client.get("/api/auth/me", headers=repairer_headers)
        repairer_id = me_resp.json()["data"]["id"]

        await client.put(
            f"/api/repairs/{repair_id}/assign",
            json={"assigned_to": repairer_id}, headers=admin_headers
        )

        # Repairer updates status to repairing
        response = await client.put(
            f"/api/repairs/{repair_id}/status",
            json={
                "status": "repairing",
                "repair_process": "Diagnosing the issue"
            }, headers=repairer_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["status"] == "repairing"

        # Repairer updates status to repaired
        response = await client.put(
            f"/api/repairs/{repair_id}/status",
            json={
                "status": "repaired",
                "repair_result": "Replaced faulty component"
            }, headers=repairer_headers
        )
        assert response.status_code == 200
        assert response.json()["data"]["status"] == "repaired"


# ---------------------------------------------------------------------------
# Confirm repair
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_confirm_repair_complete():
    """Admin confirms a repair as completed."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "confirm_rep_admin", "13830000060", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "Confirm Repair Device", "laptop")
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        # Create repair
        resp = await client.post("/api/repairs", json={
            "device_id": device_id,
            "fault_description": "Confirm test"
        }, headers=admin_headers)
        repair_id = resp.json()["data"]["id"]

        # Register repairer and assign
        repairer_token = await register_and_login(
            client, "confirm_repairer", "13830000061", "repair123", "repairer"
        )
        repairer_headers = {"Authorization": f"Bearer {repairer_token}"}
        me_resp = await client.get("/api/auth/me", headers=repairer_headers)
        repairer_id = me_resp.json()["data"]["id"]

        await client.put(
            f"/api/repairs/{repair_id}/assign",
            json={"assigned_to": repairer_id}, headers=admin_headers
        )

        # Repairer marks as repaired
        await client.put(
            f"/api/repairs/{repair_id}/status",
            json={"status": "repaired", "repair_result": "Fixed"}, headers=repairer_headers
        )

        # Admin confirms
        response = await client.put(
            f"/api/repairs/{repair_id}/confirm?action=complete", headers=admin_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["msg"] == "维修已完成"


@pytest.mark.asyncio
async def test_confirm_repair_scrap():
    """Admin confirms a repair as scrap."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "scrap_admin", "13830000070", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "Scrap Device", "laptop")
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        # Create repair
        resp = await client.post("/api/repairs", json={
            "device_id": device_id,
            "fault_description": "Beyond repair"
        }, headers=admin_headers)
        repair_id = resp.json()["data"]["id"]

        # Register repairer, assign, mark as unfixable
        repairer_token = await register_and_login(
            client, "scrap_repairer", "13830000071", "repair123", "repairer"
        )
        repairer_headers = {"Authorization": f"Bearer {repairer_token}"}
        me_resp = await client.get("/api/auth/me", headers=repairer_headers)
        repairer_id = me_resp.json()["data"]["id"]

        await client.put(
            f"/api/repairs/{repair_id}/assign",
            json={"assigned_to": repairer_id}, headers=admin_headers
        )
        await client.put(
            f"/api/repairs/{repair_id}/status",
            json={"status": "unfixable", "repair_result": "Cannot be fixed"}, headers=repairer_headers
        )

        # Admin confirms as scrap
        response = await client.put(
            f"/api/repairs/{repair_id}/confirm?action=scrap", headers=admin_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["msg"] == "设备已报废"


# ---------------------------------------------------------------------------
# Get assigned repairs (repairer)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_assigned_repairs():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "assigned_admin", "13830000080", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "Assigned Device", "laptop")
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        # Create repair
        resp = await client.post("/api/repairs", json={
            "device_id": device_id,
            "fault_description": "Assigned test"
        }, headers=admin_headers)
        repair_id = resp.json()["data"]["id"]

        # Register repairer and assign
        repairer_token = await register_and_login(
            client, "assigned_repairer", "13830000081", "repair123", "repairer"
        )
        repairer_headers = {"Authorization": f"Bearer {repairer_token}"}
        me_resp = await client.get("/api/auth/me", headers=repairer_headers)
        repairer_id = me_resp.json()["data"]["id"]

        await client.put(
            f"/api/repairs/{repair_id}/assign",
            json={"assigned_to": repairer_id}, headers=admin_headers
        )

        # Repairer lists assigned repairs
        response = await client.get("/api/repairs/assigned", headers=repairer_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert len(data["data"]["list"]) >= 1


# ---------------------------------------------------------------------------
# Filter repairs by status
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_filter_repairs_by_status():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "filter_rep_admin", "13830000090", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "Filter Repair Device", "laptop")
        headers = {"Authorization": f"Bearer {admin_token}"}

        await client.post("/api/repairs", json={
            "device_id": device_id,
            "fault_description": "Filter test"
        }, headers=headers)

        response = await client.get("/api/repairs?status=pending", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        for repair in data["data"]["list"]:
            assert repair["status"] == "pending"


# ---------------------------------------------------------------------------
# Full repair workflow (integration)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_full_repair_workflow():
    """End-to-end: create device -> create repair -> assign -> repair -> confirm."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Admin registers and creates a device
        admin_token = await register_and_login(
            client, "fullrep_admin", "13830000099", "admin123", "admin"
        )
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        device_id = await create_device(client, admin_token, "FullRepair Device", "laptop")

        # 2. Admin creates a repair order
        resp = await client.post("/api/repairs", json={
            "device_id": device_id,
            "fault_description": "Battery not charging"
        }, headers=admin_headers)
        assert resp.status_code == 200
        repair_id = resp.json()["data"]["id"]
        assert resp.json()["data"]["status"] == "pending"

        # 3. Register a repairer
        repairer_token = await register_and_login(
            client, "fullrep_repairer", "13830000100", "repair123", "repairer"
        )
        repairer_headers = {"Authorization": f"Bearer {repairer_token}"}
        me_resp = await client.get("/api/auth/me", headers=repairer_headers)
        repairer_id = me_resp.json()["data"]["id"]

        # 4. Admin assigns repairer
        resp = await client.put(
            f"/api/repairs/{repair_id}/assign",
            json={"assigned_to": repairer_id}, headers=admin_headers
        )
        assert resp.status_code == 200

        # 5. Repairer starts repairing
        resp = await client.put(
            f"/api/repairs/{repair_id}/status",
            json={"status": "repairing", "repair_process": "Replacing battery"},
            headers=repairer_headers
        )
        assert resp.status_code == 200
        assert resp.json()["data"]["status"] == "repairing"

        # 6. Repairer marks as repaired
        resp = await client.put(
            f"/api/repairs/{repair_id}/status",
            json={"status": "repaired", "repair_result": "Battery replaced"},
            headers=repairer_headers
        )
        assert resp.status_code == 200
        assert resp.json()["data"]["status"] == "repaired"

        # 7. Admin confirms
        resp = await client.put(
            f"/api/repairs/{repair_id}/confirm?action=complete",
            headers=admin_headers
        )
        assert resp.status_code == 200