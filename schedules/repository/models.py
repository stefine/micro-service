from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()


class Schedule(Base):
    __tablename__ = "schedule"
    id = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
