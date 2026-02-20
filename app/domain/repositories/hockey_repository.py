from sqlalchemy.orm import Session
from app.domain.models.hockey_team import HockeyTeam


def bulk_insert_hockey(db: Session, teams: list[dict]):
    db.bulk_insert_mappings(HockeyTeam, teams)
    db.commit()
