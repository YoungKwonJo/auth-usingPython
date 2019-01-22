from model.test import Test                 
from util.db   import db_session           
from datetime   import datetime, timedelta  
import json

def insert(nickname, password, title, contents):
  try:
    v = Test(nickname=nickname, password=password, title=title, contents=contents, date=datetime.utcnow())
    db_session.add(v)
    db_session.commit()  
    return True
  except: return False


def select(page):
  pagesize = 10;
  rows = db_session.query(Test).offset(pagesize*page).limit(pagesize)
  return json.dumps([(dict(row.items())) for row in rows])

def selectOne(id):
  out = db_session.query(Test).filter_by(id).first()
  return json.dumps([(dict(row.items())) for row in rows])


def update(id, password, nickname, title, contents):
  out = db_session.query(Test).filter_by(id, password ).first()
  if not out:
    try:
      db_session.query(Test).filter_by(id).update({"nickname":nickname,"title":title,"contents":contents,"dateLastModify":datetime.utcnow() })
      db_session.commit()   
      return True
    except: return False


def delete(id, password):
  try:
    db_session.delete(Test(id,password))
    db_session.commit()
  except: return False





