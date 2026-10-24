
import pytest
from fastapi.testclient import TestClient

from api import app


@pytest.fixture
def client(test_database):
    """Provide a test client using the isolated PostgreSQL test database."""
    with TestClient(app) as test_client:
        yield test_client


def create_sample_application(client):
    """Create an application for tests that need an existing record."""
    response = client.post(
        "/applications",
        json={
            "company": "Test Company",
            "role": "Python Developer",
            "location": "Hyderabad",
            "job_type": "Full-time",
            "salary": "12 LPA",
            "job_url": "https://example.com/jobs",
            "notes": "Created for API testing",
            "status": "Applied",
            "date_applied": "2026-10-24",
        },
    )

    assert response.status_code == 201
    return response.json()["id"]


def test_home_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.json()


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_list_applications_empty(client):
    response = client.get("/applications")

    assert response.status_code == 200
    assert response.json()["count"] == 0
    assert response.json()["applications"] == []


def test_create_application(client):
    response = client.post(
        "/applications",
        json={
            "company": "Google",
            "role": "Backend Developer",
            "date_applied": "2026-10-24",
        },
    )

    assert response.status_code == 201
    assert response.json()["id"] is not None

    applications_response = client.get("/applications")
    assert applications_response.json()["count"] == 1


def test_create_application_with_all_fields(client):
    response = client.post(
        "/applications",
        json={
            "company": "Microsoft",
            "role": "Data Analyst",
            "location": "Hyderabad",
            "job_type": "Full-time",
            "salary": "12 LPA",
            "job_url": "https://careers.microsoft.com/",
            "notes": "API test",
            "status": "Interview",
            "date_applied": "2026-10-24",
        },
    )

    assert response.status_code == 201

    application_id = response.json()["id"]
    detail_response = client.get(f"/applications/{application_id}")

    assert detail_response.status_code == 200
    assert detail_response.json()["company"] == "Microsoft"
    assert detail_response.json()["status"] == "Interview"


def test_create_application_rejects_missing_required_fields(client):
    response = client.post(
        "/applications",
        json={"company": "Google"},
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "field,value",
    [
        ("job_type", "InvalidType"),
        ("status", "InvalidStatus"),
        ("job_url", "not-a-valid-url"),
        ("date_applied", "not-a-date"),
    ],
)
def test_create_application_rejects_invalid_values(client, field, value):
    payload = {
        "company": "Test Company",
        "role": "Python Developer",
        "date_applied": "2026-10-24",
    }
    payload[field] = value

    response = client.post("/applications", json=payload)

    assert response.status_code == 422


def test_get_application_by_id(client):
    application_id = create_sample_application(client)

    response = client.get(f"/applications/{application_id}")

    assert response.status_code == 200
    assert response.json()["id"] == application_id
    assert response.json()["company"] == "Test Company"


def test_get_nonexistent_application(client):
    response = client.get("/applications/999999")

    assert response.status_code == 404


def test_search_applications(client):
    create_sample_application(client)

    response = client.get("/applications?search=Test")

    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_filter_applications_by_status(client):
    create_sample_application(client)

    response = client.get("/applications?status=Applied")

    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_filter_applications_rejects_invalid_status(client):
    response = client.get("/applications?status=InvalidStatus")

    assert response.status_code == 422


def test_sort_applications(client):
    create_sample_application(client)

    response = client.get("/applications?sort=asc")

    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_update_application_status(client):
    application_id = create_sample_application(client)

    response = client.patch(
        f"/applications/{application_id}/status",
        json={"status": "Interview"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Interview"

    detail_response = client.get(f"/applications/{application_id}")
    assert detail_response.json()["status"] == "Interview"


def test_update_application_details(client):
    application_id = create_sample_application(client)

    response = client.patch(
        f"/applications/{application_id}",
        json={"role": "Senior Python Developer"},
    )

    assert response.status_code == 200
    assert (
        response.json()["application"]["role"]
        == "Senior Python Developer"
    )
    assert response.json()["application"]["company"] == "Test Company"


def test_update_application_rejects_empty_body(client):
    application_id = create_sample_application(client)

    response = client.patch(
        f"/applications/{application_id}",
        json={},
    )

    assert response.status_code == 400


def test_update_nonexistent_application(client):
    response = client.patch(
        "/applications/999999/status",
        json={"status": "Interview"},
    )

    assert response.status_code == 404


def test_delete_application(client):
    application_id = create_sample_application(client)

    response = client.delete(f"/applications/{application_id}")

    assert response.status_code == 204

    detail_response = client.get(f"/applications/{application_id}")
    assert detail_response.status_code == 404


def test_delete_nonexistent_application(client):
    response = client.delete("/applications/999999")

    assert response.status_code == 404



def test_get_stats_empty_database(client):
    response = client.get("/stats")

    assert response.status_code == 200
    assert response.json() == {
        "total": 0,
        "applied": 0,
        "interview": 0,
        "selected": 0,
        "rejected": 0,
        "withdrawn": 0,
    }


def test_get_stats_with_applications(client):
    client.post(
        "/applications",
        json={
            "company": "Google",
            "role": "Python Developer",
            "status": "Applied",
            "date_applied": "2026-10-20",
        },
    )
    client.post(
        "/applications",
        json={
            "company": "Microsoft",
            "role": "Backend Developer",
            "status": "Interview",
            "date_applied": "2026-10-21",
        },
    )

    response = client.get("/stats")

    assert response.status_code == 200
    assert response.json() == {
        "total": 2,
        "applied": 1,
        "interview": 1,
        "selected": 0,
        "rejected": 0,
        "withdrawn": 0,
    }



def test_response_rate_empty_database(client):
    response = client.get("/stats/response-rate")

    assert response.status_code == 200
    assert response.json() == {
        "total": 0,
        "responded": 0,
        "response_rate": 0.0,
    }


def test_response_rate_with_mixed_statuses(client):
    for company, status in [
        ("Google", "Applied"),
        ("Microsoft", "Interview"),
        ("Amazon", "Rejected"),
        ("Infosys", "Selected"),
    ]:
        result = client.post(
            "/applications",
            json={
                "company": company,
                "role": "Software Developer",
                "status": status,
                "date_applied": "2026-10-24",
            },
        )
        assert result.status_code == 201

    response = client.get("/stats/response-rate")

    assert response.status_code == 200
    assert response.json() == {
        "total": 4,
        "responded": 3,
        "response_rate": 75.0,
    }


def test_response_rate_with_only_applied_status(client):
    result = client.post(
        "/applications",
        json={
            "company": "Test Company",
            "role": "Python Developer",
            "status": "Applied",
            "date_applied": "2026-10-24",
        },
    )
    assert result.status_code == 201

    response = client.get("/stats/response-rate")

    assert response.status_code == 200
    assert response.json() == {
        "total": 1,
        "responded": 0,
        "response_rate": 0.0,
    }



def test_monthly_stats_empty_database(client):
    response = client.get("/stats/monthly")

    assert response.status_code == 200
    assert response.json() == []


def test_monthly_stats_groups_applications_by_month(client):
    applications = [
        {
            "company": "Google",
            "role": "Python Developer",
            "status": "Applied",
            "date_applied": "2026-09-10",
        },
        {
            "company": "Microsoft",
            "role": "Backend Developer",
            "status": "Interview",
            "date_applied": "2026-09-25",
        },
        {
            "company": "Amazon",
            "role": "Software Developer",
            "status": "Applied",
            "date_applied": "2026-10-05",
        },
    ]

    for application in applications:
        result = client.post("/applications", json=application)
        assert result.status_code == 201

    response = client.get("/stats/monthly")

    assert response.status_code == 200
    assert response.json() == [
        {"month": "2026-09", "total": 2},
        {"month": "2026-10", "total": 1},
    ]


