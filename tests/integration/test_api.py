from unittest.mock import patch

# -----------------------------
# CRAWL ENDPOINTS
# -----------------------------


def test_schedule_hockey_job(client):
    with patch("app.domain.services.crawl_service.publish_message") as mock_publish:
        response = client.post("/crawl/hockey")

    assert response.status_code == 200
    data = response.json()

    assert "job_id" in data
    mock_publish.assert_called_once()


def test_schedule_oscar_job(client):
    with patch("app.domain.services.crawl_service.publish_message") as mock_publish:
        response = client.post("/crawl/oscar")

    assert response.status_code == 200
    data = response.json()

    assert "job_id" in data
    mock_publish.assert_called_once()


def test_schedule_all_jobs(client):
    with patch("app.domain.services.crawl_service.publish_message") as mock_publish:
        response = client.post("/crawl/all")

    assert response.status_code == 200
    data = response.json()

    assert "hockey_job_id" in data
    assert "oscar_job_id" in data
    assert mock_publish.call_count == 2


# -----------------------------
# JOB MANAGEMENT
# -----------------------------


def test_job_lifecycle(client):

    with patch("app.domain.services.crawl_service.publish_message"):
        create = client.post("/crawl/hockey")

    job_id = create.json()["job_id"]

    # get job
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200

    job = response.json()
    assert job["id"] == job_id
    assert job["status"] in ["pending", "running", "completed", "failed"]

    # list jobs
    response = client.get("/jobs")
    assert response.status_code == 200

    jobs = response.json()
    assert isinstance(jobs, list)
    assert any(j["id"] == job_id for j in jobs)


# -----------------------------
# RESULTS ENDPOINTS
# -----------------------------


def test_results_endpoints_exist(client):
    """
    Só valida que endpoints existem e não quebram.
    Não depende de worker rodando.
    """
    response = client.get("/results")
    assert response.status_code == 200

    response = client.get("/results/hockey")
    assert response.status_code == 200

    response = client.get("/results/oscar")
    assert response.status_code == 200


def test_job_results_endpoint(client):
    with patch("app.domain.services.crawl_service.publish_message"):
        create = client.post("/crawl/hockey")

    job_id = create.json()["job_id"]

    response = client.get("/jobs")
    assert response.status_code == 200
    jobs = response.json()
    assert any(j["id"] == job_id for j in jobs)

    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    job = response.json()
    assert job["id"] == job_id

    response = client.get(f"/jobs/{job_id}/results")
    assert response.status_code == 200
