from model.test import Test                 
from util.db   import db_session           
from datetime   import datetime, timedelta  
import json

def getData(data):
  return {"id":data.id, "nickname":data.nickname, "date":str(data.date), "title":data.title, "contents":data.contents }

def insert(nickname, password, title, contents):
  try:
    v = Test(nickname=nickname, password=password, title=title, contents=contents, date=datetime.utcnow())
    db_session.add(v)
    db_session.commit()   
    return True
  except: return False


def select(page):
  pagesize = 10;
  count = db_session.query(Test).count()
  if count>0:
    rows = db_session.query(Test).offset(pagesize*page).limit(pagesize).all()
    
    #print("count : "+str(count))
    #print(rows[0].nickname)
    result = [getData(row)  for row in rows]
    
    #print(result)
    return json.dumps({'count':count,'data':result}, ensure_ascii=False) #.encode('utf8')
  else:
    return json.dumps({'count':0,'data':[]})

def selectOne(id):
  row = db_session.query(Test).filter_by(id=id).first()
  #print(getData(row))
  return json.dumps(getData(row),ensure_ascii=False) #.encode('utf8')


def update(id, password, nickname, title, contents):
  try:
    out = db_session.query(Test).filter_by(id=id,password=password).first()
    #print(str(type(out)))
    if "<class 'model.test.Test'>" == str(type(out)):
      db_session.query(Test).filter_by(id=id,password=password).update({"nickname":nickname,"title":title,"contents":contents,"dateLastModify":datetime.utcnow() })
      db_session.commit()   
      return True
    else: return False
  except: return False


def delete(id, password):
  try:
    out = db_session.query(Test).filter_by(id=id, password=password ).first()
    print(str(out))
    if "<class 'model.test.Test'>" == str(type(out)):
      db_session.query(Test).filter_by(id=id, password=password ).delete()
      db_session.commit()
      return True
    else:
      print("error1") 
      return False
  except:
    print("error2")
    return False





