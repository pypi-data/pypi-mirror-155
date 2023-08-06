import logging
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class StateCounter(Base):
    __tablename__ = "state_counter"

    id = Column(Integer, primary_key=True)
    count = Column(Integer)

    def __repr__(self):
        return f'{self.count}'

    def get_base(self):
        return self.Base


def init_state_db(db_path):
    try:
        engine = create_engine(db_path)
        Base.metadata.create_all(engine)

    except Exception as e:
        logging.error(e)

    else:
        print("Database started!")
        return engine


def increment_state_counter(engine, count):
    # update_counter(engine)
    with Session(engine) as session:
        state_counter = StateCounter(count=count)
        if state_counter:
            session.add(state_counter)
            session.commit()


def reset_counter(engine):
    with Session(engine) as session:
        session.query(StateCounter).delete()
        session.commit()

    return True

def update_counter(engine):
    try:
        with Session(engine) as session:
            session.query(StateCounter).delete()
            session.commit()
    
    except Exception as e:
        logging.error(e)
        return