from model.test import Test                 
from util.db   import db_session           
from datetime   import datetime, timedelta  
import json


def checkEmail(email):
    from model.auth import Accounts

    try: 
      row = db_session.query(Accounts).filter_by(email=email).first()
      if not 'NoneType' in str(type(row)): return True
      else: return False
    except: return False

def getAccountId(email):
    from model.auth import Accounts

    try: 
      row = db_session.query(Accounts).filter_by(email=email).first()
      return row.id
    except: return False

def insertUser(email, password, nickname):
    from model.auth import Accounts, Passwords
    if not checkEmail(email):
      import uuid
      id = str(uuid.uuid4())
      try:
          v = Accounts(id=id, email=email, nickname=nickname) 
          v2 = Passwords(id=id, password=password)
          db_session.add(v)
          db_session.add(v2)
          db_session.commit()
          
          return True
      except: return False
    else: return False

def loginUser(email):
    from model.auth import Accounts, Passwords
    try:
      row = db_session.query(Accounts).filter_by(email=email).join(Passwords, Accounts.id == Passwords.id).first()
      row2 = db_session.query(Passwords).join(Accounts, Passwords.id == Accounts.id).filter_by(email=email).first()

      if not 'NoneType' in str(type(row)) and not 'NoneType' in str(type(row2)):
          return {'password':row2.password,'email':row.email,'nickname':row.nickname, 'accountid':row.id}
    except: return ''


