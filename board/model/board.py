from sqlalchemy import Column, Integer, String, DateTime, Boolean, Index

from util.db import Base, engine
from datetime import datetime

class Board(Base):
    __tablename__ = 'Board'
    id             = Column( Integer, primary_key=True, autoincrement=True)
    date           = Column( DateTime, default=datetime.utcnow, nullable=False)
    nickname       = Column( String(50), nullable=False)
    accountid      = Column( String(50), nullable=False)
    title          = Column( String(100), nullable=False)
    contents       = Column( String(1000), nullable=False)
    dateLastModify = Column( DateTime, default=datetime.utcnow)

    __table_args__ = (
       Index('test_idx_id_date_nickname_title', 'id', 'date', 'nickname','title'),
    )


def init_db():
    Base.metadata.create_all(bind=engine)
