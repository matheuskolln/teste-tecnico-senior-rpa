from app.infrastructure.db.base import Base
from sqlalchemy import ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
import uuid

class JobResult(Base):
    __tablename__ = "job_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id"),
        nullable=False,
        index=True,
    )

    data: Mapped[dict] = mapped_column(JSON)
