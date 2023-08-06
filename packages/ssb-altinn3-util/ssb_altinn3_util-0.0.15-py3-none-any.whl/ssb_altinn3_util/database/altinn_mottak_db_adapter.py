from pg8000.dbapi import Connection
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from google.cloud.sql.connector import connector


class AltinnMottakDbAdapter:
    Base = declarative_base()

    def __init__(self):
        self.engine = None
        self.session_provider = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def get_session(self) -> Session:
        db = self.session_provider()
        try:
            yield db
        finally:
            db.close()

    def init_engine(
        self,
        user_name: str,
        database_name: str,
        user_password: str,
        project_id: str,
        spanner_instance_id: str,
    ):
        if spanner_instance_id:
            self.engine = create_engine(
                f"spanner+spanner:///projects/{project_id}/instances/{spanner_instance_id}/databases/{database_name}"
            )
        else:
            self.engine = create_engine(
                f"postgresql+pg8000://{user_name}:{user_password}@localhost:5432/{database_name}"
            )
