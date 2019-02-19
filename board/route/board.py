import json
from flask import render_template, request

import uuid
from datetime import datetime, timedelta

from route.base import postData, errror, headerAuth, referer, doIt

from action.board import insert, select, update, delete, selectOne 


def board(app):
  @app.route("/board")
  def board():
    return "board route"

 
  @app.route("/board/error", methods=['POST'])
  def error2():
     #import json
     return json.dumps({"error":"error"}),404
  
  ## 추가하기 POST
  @app.route("/board/insert", methods=['POST'])
  def insertPost2():
    data = postData()

    header = headerAuth()
    #print(header)
    if not "access" in header['type']:  return json.dumps({"status":"fail---"})

    #print(data)
    #print(data.keys())
    if 'nickname' in header.keys() and 'accountid' in header.keys() and 'title' in data.keys() and 'contents' in data.keys():
      if insert(nickname=header['nickname'], accountid=header['accountid'], title=data['title'], contents=data['contents']):
        return json.dumps({"status":"success"})
      else:  return json.dumps({"status":"fail2"})
    else:  return json.dumps({"status":"fail1"})

  ## 데이터 읽기 GET
  @app.route("/board/list")
  def selectPost2():
    header = headerAuth()
    if not "access" in header['type']:  return json.dumps({"status":"fail"})

    page = request.args.get('page', default = 0, type = int)
    #print(page)
    try:
      return select(page=page)
    except:
      return json.dumps({"status":"fail"})

  ## 데이터 읽기 GET
  @app.route("/board/article")
  def selectOnePost2():
    header = headerAuth()
    if not "access" in header['type']:  return json.dumps({"status":"fail"})

    id = request.args.get('id', default = 0, type = int)
    #print(id)
    try:
      return selectOne(id=id)
    except:
      return json.dumps({"status":"fail"})



 ## 데이터 업데이트 하기 POST
  @app.route("/board/update", methods=['POST'])
  def updatePost2():
    header = headerAuth()
    if not "access" in header['type']:  return json.dumps({"status":"fail"})

    data = postData()
    #print(data)
    #print(data.keys())
    if 'id' in data.keys() and 'nickname' in header.keys() and 'accountid' in header.keys() and 'title' in data.keys() and 'contents' in data.keys():
      return doIt(update(id=data['id'],nickname=header['nickname'], accountid=header['accountid'], title=data['title'], contents=data['contents']))
    else:  return json.dumps({"status":"fail1"})

 ## 데이터 삭제 하기 POST
  @app.route("/board/delete", methods=['POST'])
  def deletePost2():
    header = headerAuth()
    if not "access" in header['type']:  return json.dumps({"status":"fail"})
    print(header)

    data = postData()
    if 'id' in data.keys() and 'accountid' in header.keys():
      return doIt(delete(id=data['id'], accountid=header['accountid']))
    else: return json.dumps({"status":"fail1"})


