from unittest.mock import patch


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
