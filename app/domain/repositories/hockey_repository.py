from sqlalchemy.orm import Session
from app.domain.models.hockey_team import HockeyTeam

from sqlalchemy.dialects.postgresql import insert

def bulk_insert_hockey(db: Session, teams: list[dict]):
    if not teams:
        return

    stmt = insert(HockeyTeam).values(teams)

    stmt = stmt.on_conflict_do_nothing(index_elements=['team_name', 'year'])

    try:
        db.execute(stmt)
        db.commit()
    except Exception:
        db.rollback()
        raise
