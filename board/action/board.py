from model.board import Board                 
from util.db   import db_session           
from datetime   import datetime, timedelta  
import json

def getData(data):
  return {"id":data.id, "nickname":data.nickname, "date":str(data.date), "title":data.title, "contents":data.contents }

def insert(nickname, accountid, title, contents):
  try:
    v = Board(nickname=nickname, accountid=accountid, title=title, contents=contents, date=datetime.utcnow())
    db_session.add(v)
    db_session.commit()   
    return True
  except: return False


def select(page):
  pagesize = 10;
  count = db_session.query(Board).count()
  if count>0:
    rows = db_session.query(Board).offset(pagesize*page).limit(pagesize).all()
    
    print("count : "+str(count))
    
    #print(rows[0].nickname)
    result = [getData(row)  for row in rows]
    
    #print(result)
    return json.dumps({'count':count,'data':result}, ensure_ascii=False)#.encode('utf8')
  else:
    return json.dumps({'count':0,'data':[]})

def selectOne(id):
  row = db_session.query(Board).filter_by(id=id).first()
  return json.dumps([getData(row)],ensure_ascii=False)#.encode('utf8')


def update(id, accountid, nickname, title, contents):
  try:
    out = db_session.query(Board).filter_by(id=id,accountid=accountid).first()
    print(str(type(out)))
    if "<class 'model.board.Board'>" == str(type(out)):
      db_session.query(Board).filter_by(id=id,accountid=accountid).update({"nickname":nickname,"title":title,"contents":contents,"dateLastModify":datetime.utcnow() })
      db_session.commit()   
      return True
    else: return False
  except: return False


def delete(id, accountid):
  try:
    out = db_session.query(Board).filter_by(id=id,accountid=accountid ).first()
    print(out)
    if "<class 'model.board.Board'>" == str(type(out)):
      db_session.query(Board).filter_by(id=id,accountid=accountid ).delete()
      db_session.commit()
      return True
    else:
      print("error1") 
      return False
  except:
    print("error2")
    return False





