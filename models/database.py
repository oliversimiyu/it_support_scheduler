from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class TeamMember(Base):
    __tablename__ = 'team_members'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    availability = Column(String)  # Stored as comma-separated days
    shifts = relationship("Shift", back_populates="team_member")

class Shift(Base):
    __tablename__ = 'shifts'
    
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    shift_type = Column(String, nullable=False)  # Morning, Afternoon, Night
    team_member_id = Column(Integer, ForeignKey('team_members.id'))
    team_member = relationship("TeamMember", back_populates="shifts")

def init_db():
    engine = create_engine('sqlite:///data/scheduler.db')
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
