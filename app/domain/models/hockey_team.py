from sqlalchemy import Column, Integer, String, Float
from app.infrastructure.db.base import Base


class HockeyTeam(Base):
    __tablename__ = "hockey_teams"

    id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String)
    year = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    ot_losses = Column(Integer)
    win_pct = Column(Float)
    goals_for = Column(Integer)
    goals_against = Column(Integer)
    goal_diff = Column(Integer)
