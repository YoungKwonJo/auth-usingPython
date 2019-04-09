import json
from flask import render_template, request
from flask_restplus import Api, Resource, fields

import uuid
from datetime import datetime, timedelta

from route.base import postData, errror, headerAuth, referer, doIt

from action.board import insert, select, update, delete, selectOne 


def board(app):

  model = app.model("insertArticleWithAuth",
   {
   "title": fields.String(required = True, description="제목", help="Write a title"),
   "contents": fields.String(required = True, description="내용", help="Write a contents"),
   })
  model2 = app.model("ModifyArticleWithAuth",
   {
   "id": fields.Integer(required = True, description="글번호", help="Write a number for a article"),
   "title": fields.String(required = True, description="제목", help="Write a title"),
   "contents": fields.String(required = True, description="내용", help="Write a contents"),
   })
  model3 = app.model("DeleteArticleWithAuth",
   {
   "id": fields.Integer(required = True, description="글번호", help="Write a number for a article"),
   })
 

  @app.route("/board")
  @app.doc(params={})
  class Board(Resource):
    def get(self):
      return "board route"

  ## 추가하기 POST
  @app.route("/board/insert", methods=['POST'])
  @app.expect(model)
  class InsertPost2(Resource):
    @app.doc(security='apikey')
    def post(self):
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
  @app.doc(params={'page':'페이저 번호'})
  class SelectPost2(Resource):
    @app.doc(security='apikey')
    def get(self):
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
  @app.doc(params={'id':' 글번호'})
  class SelectOnePost2(Resource):
    @app.doc(security='apikey')
    def get(self):
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
  @app.expect(model2)
  class UpdatePost2(Resource):
    @app.doc(security='apikey')
    def post(self):
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
  @app.expect(model3)
  class DeletePost2(Resource):
    @app.doc(security='apikey')
    def post(self):
      header = headerAuth()
      if not "access" in header['type']:  return json.dumps({"status":"fail"})
      print(header)
      
      data = postData()
      if 'id' in data.keys() and 'accountid' in header.keys():
        return doIt(delete(id=data['id'], accountid=header['accountid']))
      else: return json.dumps({"status":"fail1"})

