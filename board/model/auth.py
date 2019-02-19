from sqlalchemy import Column, Integer, String, DateTime, Boolean, Index

from util.db import Base, engine
from datetime import datetime

class Accounts(Base):
    __tablename__ = 'MyAccounts'
    id             = Column( String(50), primary_key=True)
    email          = Column( String(100), primary_key=True)

    dateSigin      = Column( DateTime, default=datetime.utcnow)
    date           = Column( DateTime, default=datetime.utcnow)

    nickname       = Column( String(50), nullable=False)
    #password       = Column( String(150),nullable=False)

    __table_args__ = (
       Index('myaccounts_id_email_nickname', 'id', 'email', 'nickname'),
    )

class Passwords(Base):
    __tablename__ = 'MyPasswords'
    id             = Column( String(50), primary_key=True)
    password       = Column( String(200),nullable=False)

    __table_args__ = (
       Index('mypasswords_id_password', 'id', 'password'),
    )


def init_db():
    Base.metadata.create_all(bind=engine)
