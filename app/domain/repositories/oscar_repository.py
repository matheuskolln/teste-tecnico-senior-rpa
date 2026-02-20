from sqlalchemy.orm import Session
from app.domain.models.oscar_film import OscarFilm


def bulk_insert_oscar(db: Session, films: list[dict]):
    db.bulk_insert_mappings(OscarFilm, films)
    db.commit()
