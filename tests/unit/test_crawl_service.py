import pytest
from unittest.mock import AsyncMock, patch

from app.domain.services.crawl_service import schedule_crawl
from app.domain.models.job import JobType


@pytest.mark.asyncio
async def test_schedule_crawl_publishes_message(db_session):
    with patch(
        "app.domain.services.crawl_service.publish_message",
        new_callable=AsyncMock,
    ) as mock_publish:

        job = await schedule_crawl(db_session, JobType.hockey)

        assert job.id is not None
        mock_publish.assert_called_once()

        args = mock_publish.call_args[1]
        assert args["queue_name"] == "hockey_queue"


@pytest.mark.asyncio
async def test_schedule_crawl_publish_error(db_session):
    with patch(
        "app.domain.services.crawl_service.publish_message",
        side_effect=Exception("rabbit error"),
    ):
        with pytest.raises(Exception):
            await schedule_crawl(db_session, JobType.hockey)
