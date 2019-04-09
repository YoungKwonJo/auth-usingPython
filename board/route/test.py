import json
from flask import render_template, request
from flask_restplus import Api, Resource, fields

import uuid
from datetime import datetime, timedelta

from route.base import postData, errror, headerAuth, referer

from action.test import insert, select, update, delete, selectOne 


def test(app):

  model = app.model("NewArticle",
   {
   "nickname": fields.String(required = True, description="이름", help="Write a name"),
   "password": fields.String(required = True, description="패스워드", help="Write a password"),
   "title":    fields.String(required = True, description="제목", help="Write a  title"),
   "contents": fields.String(required = True, description="내용", help="Write a contents"),
   })
  model2 = app.model("ModifyArticle",
   {
   "id":       fields.Integer(required = True, description="글번호", help="Write a number for a article"),
   "nickname": fields.String(required = True, description="이름", help="Write a name"),
   "password": fields.String(required = True, description="패스워드", help="Write a password"),
   "title":    fields.String(required = True, description="제목", help="Write a  title"),
   "contents": fields.String(required = True, description="내용", help="Write a contents"),
   })
  model3 = app.model("DeleteArticle",
   {
   "id":       fields.Integer(required = True, description="글번호", help="Write a number for a article"),
   "password": fields.String(required = True, description="패스워드", help="Write a password"),
   })

  @app.route("/test")
  @app.doc(params={})
  class Test(Resource):
    def get(self):
      return "test route"

 
  ## 추가하기 POST
  @app.route("/insert", methods=['POST'])
  @app.expect(model)
  class InsertPost(Resource):
    def post(self): 
      data = postData()
      print(data)
      print(data.keys())
      #print(data)
      #print(data.keys())
      if 'nickname' in data.keys() and 'password' in data.keys() and 'title' in data.keys() and 'contents' in data.keys():
        if insert(nickname=data['nickname'], password=data['password'], title=data['title'], contents=data['contents']):
          return json.dumps({"status":"success"})
        else:  return json.dumps({"status":"fail2"})
      else:  return json.dumps({"status":"fail1"})

  ## 데이터 읽기 GET
  @app.route("/list")
  @app.doc(params={'page':'페이지 넘버'})
  class SelectGet(Resource):
    def get(self):
      page = request.args.get('page', default = 0, type = int)
      print(page)
      try:
        return select(page=page)
      except:
        return json.dumps({"status":"fail"})



  ## 데이터 읽기 GET
  @app.route("/article")
  @app.doc(params={'id':'글 넘버'})
  class SelectOnePost(Resource):
    def get(self):
      id = request.args.get('id', default = 0, type = int)
      print(id)
      #try:
      return selectOne(id=id)
      #except:
      #  return json.dumps({"status":"fail"})


  ## 데이터 업데이트 하기 POST
  @app.route("/update", methods=['POST'])
  @app.expect(model2)
  class UpdatePost(Resource):
    def post(self):
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
  @app.expect(model3)
  class DeletePost(Resource):
    def post(self):
      data = postData()
      if 'id' in data.keys() and 'password' in data.keys():
        if(delete(id=data['id'],password=data['password'])):
          return json.dumps({"status":"success"})
        else: return json.dumps({"status":"fail2"})
      else: return json.dumps({"status":"fail1"})

