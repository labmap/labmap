from typing import NamedTuple, List, Dict

import sqlalchemy.engine
from sqlalchemy import Column, Text, create_engine, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()


class Computer(Base):
    __tablename__ = 'Computers'
    id = Column(Text, primary_key=True)
    room = Column(Integer, nullable=False)
    state = Column(Text, default='off', nullable=False)
    user = Column(Text, default=None, nullable=True)

    def as_dict(self) -> Dict:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Room(NamedTuple):
    id: int
    color: str
    start_id: int = 0
    computers_count: int = 16

    def computers(self) -> List[Computer]:
        computer_indices = [str(self.start_id + i).zfill(2) for i in range(self.computers_count)]
        computer_ids = [f'{self.color}{computer_id}'for computer_id in computer_indices]
        return [Computer(id=computer_id, room=self.id) for computer_id in computer_ids]


def initialize_database(path: str) -> Session:
    engine = create_engine(f'sqlite:///{path}')
    create_missing_tables(engine)
    session = sessionmaker(bind=engine)()
    populate_database(session)
    return session


def create_missing_tables(engine: sqlalchemy.engine.Engine) -> None:
    Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=True)


def populate_database(session: Session):
    exists = session.query(Computer).first()
    if not exists:
        computers = get_initial_computers()
        session.add_all(computers)
        session.flush()


def get_initial_computers():
    rooms = [
        Room(2041, 'red'),
        Room(2042, 'pink', computers_count=18),
        Room(2043, 'orange'),
        Room(2044, 'brown'),
        Room(2045, 'yellow'),
        Room(3041, 'khaki', start_id=1),
        Room(3042, 'green'),
        Room(3043, 'cyan'),
        Room(3044, 'blue'),
        Room(3045, 'violet')
    ]
    return [computer for room in rooms for computer in room.computers()]
