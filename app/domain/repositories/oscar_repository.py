from sqlalchemy.orm import Session
from app.domain.models.oscar_film import OscarFilm

from sqlalchemy.dialects.postgresql import insert


def bulk_insert_oscar(db: Session, films: list[dict]):
    if not films:
        return

    stmt = insert(OscarFilm).values(films)

    stmt = stmt.on_conflict_do_nothing(index_elements=["title", "year"])

    try:
        db.execute(stmt)
        db.commit()
    except Exception:
        db.rollback()
        raise
