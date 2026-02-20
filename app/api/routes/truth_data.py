from app.domain.models.oscar_film import OscarFilm
from app.domain.models.hockey_team import HockeyTeam
from app.infrastructure.db.deps import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/results", tags=["results"])


@router.get("/")
def get_results(db: Session = Depends(get_db)):
    oscar_films = db.query(OscarFilm).all()
    hockey_teams = db.query(HockeyTeam).all()
    return {"oscar_films": oscar_films, "hockey_teams": hockey_teams}


@router.get("/oscar")
def get_oscar_results(db: Session = Depends(get_db)):
    oscar_films = db.query(OscarFilm).all()
    return oscar_films


@router.get("/hockey")
def get_hockey_results(db: Session = Depends(get_db)):
    hockey_teams = db.query(HockeyTeam).all()
    return hockey_teams
