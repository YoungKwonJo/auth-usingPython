import json
from flask import render_template, request

import uuid
from datetime import datetime, timedelta

from route.base import postData, errror, headerAuth, referer

from action.test import insert, select, update, delete 


def test(app):
  @app.route("/test")
  def test():
    return "test route"

 
  @app.route("/error", methods=['POST'])
  def error():
     #import json
     return json.dumps({"error":"error"}),404
  
  ## 추가하기 POST
  @app.route("/insert", methods=['POST'])
  def insertPost():
    data = postData()
    print(data)
    print(data.keys())
    if 'nickname' in data.keys() and 'password' in data.keys() and 'title' in data.keys() and 'contents' in data.keys():
      if insert(nickname=data['nickname'], password=data['password'], title=data['title'], contents=data['contents']):
        return json.dumps({"status":"success"})
      else:  return json.dumps({"status":"fail2"})
    else:  return json.dumps({"status":"fail1"})

  ## 데이터 읽기 GET
  @app.route("/list")
  def selectPost():
    page = request.args.get('page', default = 1, type = int)
    print(page)

    return json.dumps({"status":page})


 ## 데이터 업데이트 하기 POST
  @app.route("/update", methods=['POST'])
  def updatePost():
    data = postData()
    print(data)
    print(data.keys())
    if 'id' in data.keys() and 'nickname' in data.keys() and 'password' in data.keys() and 'title' in data.keys() and 'contents' in data.keys():
      if update(id=data['id'],nickname=data['nickname'], password=data['password'], title=data['title'], contents=data['contents']):
        return json.dumps({"status":"success"})
      else:  return json.dumps({"status":"fail2"})
    else:  return json.dumps({"status":"fail1"})

 ## 데이터 삭제 하기 POST
  @app.route("/delete", methods=['POST'])
  def deletePost():
    data = postData()
    if 'id' in data.keys() and 'password' in data.keys():
      delete(id=data['id'],password=data['password'])


