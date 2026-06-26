import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from tests.conftest import register_and_login, create_device


# ---------------------------------------------------------------------------
# Audit logs for borrow
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_audit_logs_for_borrow():
    """Audit logs should be created when a borrow is audited."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "auditlog_admin", "13840000001", "admin123", "admin"
        )
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        device_id = await create_device(client, admin_token, "AuditLog Device", "laptop")

        # Create a student and a borrow
        student_token = await register_and_login(
            client, "auditlog_stu", "13840000002", "pass123", "student"
        )
        stu_headers = {"Authorization": f"Bearer {student_token}"}

        resp = await client.post("/api/borrows", json={
            "device_id": device_id,
            "borrow_reason": "Audit log test"
        }, headers=stu_headers)
        borrow_id = resp.json()["data"]["id"]

        # Approve the borrow (this should create audit logs)
        await client.put(
            f"/api/borrows/{borrow_id}/audit",
            json={"action": "approve", "remark": "OK"}, headers=admin_headers
        )

        # Query audit logs
        response = await client.get(
            f"/api/audit-logs?target_type=borrow&target_id={borrow_id}",
            headers=admin_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "list" in data["data"]
        assert "total" in data["data"]
        assert data["data"]["total"] >= 1


# ---------------------------------------------------------------------------
# Audit logs for repair
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_audit_logs_for_repair():
    """Audit logs should be created during repair workflow."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "auditrep_admin", "13840000010", "admin123", "admin"
        )
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        device_id = await create_device(client, admin_token, "AuditRepair Device", "laptop")

        # Create repair
        resp = await client.post("/api/repairs", json={
            "device_id": device_id,
            "fault_description": "Audit log repair test"
        }, headers=admin_headers)
        repair_id = resp.json()["data"]["id"]

        # Register repairer and assign
        repairer_token = await register_and_login(
            client, "auditrep_repairer", "13840000011", "repair123", "repairer"
        )
        repairer_headers = {"Authorization": f"Bearer {repairer_token}"}
        me_resp = await client.get("/api/auth/me", headers=repairer_headers)
        repairer_id = me_resp.json()["data"]["id"]

        await client.put(
            f"/api/repairs/{repair_id}/assign",
            json={"assigned_to": repairer_id}, headers=admin_headers
        )

        # Query audit logs for repair
        response = await client.get(
            f"/api/audit-logs?target_type=repair&target_id={repair_id}",
            headers=admin_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "list" in data["data"]


# ---------------------------------------------------------------------------
# Unauthorized access
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_audit_logs_unauthorized():
    """No token provided."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/audit-logs?target_type=borrow&target_id=1")
        assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_audit_logs_as_student_forbidden():
    """Students cannot access audit logs."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        student_token = await register_and_login(
            client, "audit_stu_forbidden", "13840000020", "pass123", "student"
        )
        headers = {"Authorization": f"Bearer {student_token}"}
        response = await client.get(
            "/api/audit-logs?target_type=borrow&target_id=1", headers=headers
        )
        assert response.status_code == 403


# ---------------------------------------------------------------------------
# Nonexistent target
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_audit_logs_empty():
    """Query audit logs for a target that has no logs."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "audit_empty_admin", "13840000030", "admin123", "admin"
        )
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.get(
            "/api/audit-logs?target_type=borrow&target_id=99999", headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["total"] == 0
        assert len(data["data"]["list"]) == 0


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_audit_logs_pagination():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        admin_token = await register_and_login(
            client, "audit_page_admin", "13840000040", "admin123", "admin"
        )
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        device_id = await create_device(client, admin_token, "AuditPage Device", "laptop")

        # Create and approve a borrow
        student_token = await register_and_login(
            client, "audit_page_stu", "13840000041", "pass123", "student"
        )
        stu_headers = {"Authorization": f"Bearer {student_token}"}

        resp = await client.post("/api/borrows", json={
            "device_id": device_id,
            "borrow_reason": "Pagination test"
        }, headers=stu_headers)
        borrow_id = resp.json()["data"]["id"]

        await client.put(
            f"/api/borrows/{borrow_id}/audit",
            json={"action": "approve"}, headers=admin_headers
        )

        response = await client.get(
            f"/api/audit-logs?target_type=borrow&target_id={borrow_id}&page=1&page_size=5",
            headers=admin_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["page"] == 1
        assert data["data"]["page_size"] == 5