from sqlalchemy import Column, Integer, String, Boolean
from app.infrastructure.db.base import Base


class OscarFilm(Base):
    __tablename__ = "oscar_films"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    title = Column(String)
    nominations = Column(Integer)
    awards = Column(Integer)
    best_picture = Column(Boolean)
