from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path


class UnitOfWork:
    def __init__(self):
        path = "sqlite:///" + str(Path(__file__).parent/"../schedules.db")
        self.session_maker = sessionmaker(bind=create_engine(path))

    def __enter__(self):
        self.session = self.session_maker()
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type is not None:
            self.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
