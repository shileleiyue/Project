import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from tests.conftest import register_and_login, create_device


# ---------------------------------------------------------------------------
# Borrow creation
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_create_borrow():
    """Student creates a borrow request for an existing device."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Setup: admin creates a device
        admin_token = await register_and_login(
            client, "borrow_admin", "13820000001", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "Borrowable Device", "laptop")

        # Student creates borrow
        student_token = await register_and_login(
            client, "borrow_stu", "13820000002", "pass123", "student"
        )
        headers = {"Authorization": f"Bearer {student_token}"}
        response = await client.post("/api/borrows", json={
            "device_id": device_id,
            "borrow_reason": "Need for class project"
        }, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["device_id"] == device_id
        assert data["data"]["status"] == "pending"


@pytest.mark.asyncio
async def test_create_borrow_nonexistent_device():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        student_token = await register_and_login(
            client, "borrow_404_stu", "13820000003", "pass123", "student"
        )
        headers = {"Authorization": f"Bearer {student_token}"}
        response = await client.post("/api/borrows", json={
            "device_id": 99999,
            "borrow_reason": "Testing"
        }, headers=headers)
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_borrow_as_admin_forbidden():
    """Admin cannot create borrow requests (only students can)."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "borrow_as_admin", "13820000004", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "Admin Device", "tablet")

        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.post("/api/borrows", json={
            "device_id": device_id,
            "borrow_reason": "Testing"
        }, headers=headers)
        assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_borrow_unauthorized():
    """No token provided."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/borrows", json={
            "device_id": 1,
            "borrow_reason": "Testing"
        })
        assert response.status_code == 403


# ---------------------------------------------------------------------------
# Get my borrows
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_my_borrows():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "my_borrow_admin", "13820000010", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "My Device", "laptop")

        student_token = await register_and_login(
            client, "my_borrow_stu", "13820000011", "pass123", "student"
        )
        headers = {"Authorization": f"Bearer {student_token}"}

        # Create a borrow
        await client.post("/api/borrows", json={
            "device_id": device_id,
            "borrow_reason": "For my records"
        }, headers=headers)

        # Get my borrows
        response = await client.get("/api/borrows/my", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "list" in data["data"]
        assert len(data["data"]["list"]) >= 1


# ---------------------------------------------------------------------------
# Get all borrows (admin only)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_borrows_as_admin():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "all_borrow_admin", "13820000020", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "All Borrows Device", "laptop")

        # Create a student and a borrow
        student_token = await register_and_login(
            client, "all_borrow_stu", "13820000021", "pass123", "student"
        )
        await client.post("/api/borrows", json={
            "device_id": device_id,
            "borrow_reason": "Test"
        }, headers={"Authorization": f"Bearer {student_token}"})

        # Admin lists borrows
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.get("/api/borrows", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "list" in data["data"]


@pytest.mark.asyncio
async def test_get_borrows_as_student_forbidden():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        student_token = await register_and_login(
            client, "list_borrow_stu", "13820000022", "pass123", "student"
        )
        headers = {"Authorization": f"Bearer {student_token}"}
        response = await client.get("/api/borrows", headers=headers)
        assert response.status_code == 403


# ---------------------------------------------------------------------------
# Audit borrow (approve / reject)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_audit_borrow_approve():
    """Admin approves a borrow request."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "audit_approve_admin", "13820000030", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "Approve Device", "laptop")

        student_token = await register_and_login(
            client, "audit_approve_stu", "13820000031", "pass123", "student"
        )
        stu_headers = {"Authorization": f"Bearer {student_token}"}

        # Create borrow
        resp = await client.post("/api/borrows", json={
            "device_id": device_id,
            "borrow_reason": "Please approve"
        }, headers=stu_headers)
        borrow_id = resp.json()["data"]["id"]

        # Admin approves
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.put(
            f"/api/borrows/{borrow_id}/audit", json={
                "action": "approve",
                "remark": "Approved for testing"
            }, headers=admin_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["status"] == "borrowing"


@pytest.mark.asyncio
async def test_audit_borrow_reject():
    """Admin rejects a borrow request."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "audit_reject_admin", "13820000040", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "Reject Device", "laptop")

        student_token = await register_and_login(
            client, "audit_reject_stu", "13820000041", "pass123", "student"
        )
        stu_headers = {"Authorization": f"Bearer {student_token}"}

        resp = await client.post("/api/borrows", json={
            "device_id": device_id,
            "borrow_reason": "Will be rejected"
        }, headers=stu_headers)
        borrow_id = resp.json()["data"]["id"]

        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.put(
            f"/api/borrows/{borrow_id}/audit", json={
                "action": "reject",
                "remark": "Not available"
            }, headers=admin_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"] == "rejected"


# ---------------------------------------------------------------------------
# Return borrow
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_return_borrow():
    """Student returns a borrowed device."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "return_admin", "13820000050", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "Return Device", "laptop")

        student_token = await register_and_login(
            client, "return_stu", "13820000051", "pass123", "student"
        )
        stu_headers = {"Authorization": f"Bearer {student_token}"}
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        # Create borrow
        resp = await client.post("/api/borrows", json={
            "device_id": device_id,
            "borrow_reason": "Will return"
        }, headers=stu_headers)
        borrow_id = resp.json()["data"]["id"]

        # Admin approves
        await client.put(
            f"/api/borrows/{borrow_id}/audit",
            json={"action": "approve"}, headers=admin_headers
        )

        # Student returns
        response = await client.put(
            f"/api/borrows/{borrow_id}/return",
            json={"return_status": "normal"}, headers=stu_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200


# ---------------------------------------------------------------------------
# Confirm return
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_confirm_return():
    """Admin confirms a returned device."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "confirm_admin", "13820000060", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "Confirm Device", "laptop")

        student_token = await register_and_login(
            client, "confirm_stu", "13820000061", "pass123", "student"
        )
        stu_headers = {"Authorization": f"Bearer {student_token}"}
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        # Create borrow
        resp = await client.post("/api/borrows", json={
            "device_id": device_id,
            "borrow_reason": "Full cycle"
        }, headers=stu_headers)
        borrow_id = resp.json()["data"]["id"]

        # Approve
        await client.put(
            f"/api/borrows/{borrow_id}/audit",
            json={"action": "approve"}, headers=admin_headers
        )

        # Return
        await client.put(
            f"/api/borrows/{borrow_id}/return",
            json={"return_status": "normal"}, headers=stu_headers
        )

        # Confirm return
        response = await client.put(
            f"/api/borrows/{borrow_id}/confirm-return", headers=admin_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200


# ---------------------------------------------------------------------------
# Full borrow workflow (integration)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_full_borrow_workflow():
    """End-to-end: create device -> borrow -> approve -> return -> confirm."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Admin registers and creates a device
        admin_token = await register_and_login(
            client, "fullflow_admin", "13820000070", "admin123", "admin"
        )
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        device_id = await create_device(client, admin_token, "FullFlow Device", "laptop")

        # 2. Student registers
        student_token = await register_and_login(
            client, "fullflow_stu", "13820000071", "pass123", "student"
        )
        stu_headers = {"Authorization": f"Bearer {student_token}"}

        # 3. Student creates borrow request
        resp = await client.post("/api/borrows", json={
            "device_id": device_id,
            "borrow_reason": "End-to-end test"
        }, headers=stu_headers)
        assert resp.status_code == 200
        borrow_id = resp.json()["data"]["id"]
        assert resp.json()["data"]["status"] == "pending"

        # 4. Admin approves
        resp = await client.put(
            f"/api/borrows/{borrow_id}/audit",
            json={"action": "approve", "remark": "ok"}, headers=admin_headers
        )
        assert resp.status_code == 200

        # 5. Student returns
        resp = await client.put(
            f"/api/borrows/{borrow_id}/return",
            json={"return_status": "normal"}, headers=stu_headers
        )
        assert resp.status_code == 200

        # 6. Admin confirms
        resp = await client.put(
            f"/api/borrows/{borrow_id}/confirm-return", headers=admin_headers
        )
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Damaged return
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_damaged_return():
    """Student returns device as damaged."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "damage_admin", "13820000080", "admin123", "admin"
        )
        device_id = await create_device(client, admin_token, "Damage Device", "laptop")

        student_token = await register_and_login(
            client, "damage_stu", "13820000081", "pass123", "student"
        )
        stu_headers = {"Authorization": f"Bearer {student_token}"}
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        # Create and approve borrow
        resp = await client.post("/api/borrows", json={
            "device_id": device_id,
            "borrow_reason": "Damage test"
        }, headers=stu_headers)
        borrow_id = resp.json()["data"]["id"]

        await client.put(
            f"/api/borrows/{borrow_id}/audit",
            json={"action": "approve"}, headers=admin_headers
        )

        # Return as damaged
        response = await client.put(
            f"/api/borrows/{borrow_id}/return",
            json={
                "return_status": "damaged",
                "damage_description": "Screen cracked"
            }, headers=stu_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["return_status"] == "damaged"