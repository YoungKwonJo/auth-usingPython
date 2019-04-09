import json
from flask import render_template, request
from flask_restplus import Api, Resource, fields

import uuid
from datetime import datetime, timedelta

from route.base import postData, errror, headerAuth, referer, doIt
from action.auth import checkEmail, insertUser, loginUser

def auth(app):
  model = app.model("checkEmail",
   {
   "email": fields.String(required = True, description="이메일", help="Write a email"),
   })
  model2 = app.model("signIn",
   {
   "email":    fields.String(required = True, description="이메일", help="Write a email"),
   "nickname":    fields.String(required = True, description="이름", help="Write a nickname"),
   "password": fields.String(required = True, description="패스워드", help="Write a password"),
   })
  model3 = app.model("logIn",
   {
   "email":    fields.String(required = True, description="이메일", help="Write a email"),
   "password": fields.String(required = True, description="패스워드", help="Write a password"),
   })  
  model4 = app.model("refreshToken",
   {
   "token":    fields.String(required = True, description="token", help="Write a refresh"),
   #"jti":      fields.String(required = True, description="jti", help="Write a jti"),
   })


  @app.route("/auth/")
  @app.doc(params={})
  class Test1(Resource):
    def get(self):
      return "test route"


  ## 가입여부 확인 
  @app.route("/auth/checkemail", methods=['POST'])
  ### @app.header('Authorization', 'Use Bearertoken')
  @app.expect(model)
  class Checkemail(Resource):
    def post(self):
      data = postData()
      if 'email' in data.keys():
        return doIt(checkEmail(email=data['email']))
      else:  return json.dumps({"status":"fail1"})
 

  ## 가입하기 
  @app.route("/auth/signin", methods=['POST'])
  @app.expect(model2)
  class Signin(Resource):
    def post(self):
      data = postData()
      if 'nickname' in data.keys() and 'email' in data.keys() and 'password' in data.keys():
        from util.password import hash_password
        password= hash_password(data['password'])
        return doIt(insertUser(nickname=data['nickname'],email=data['email'], password=password) )
        #return doIt(insertUser(nickname=data['nickname'],email=data['email'], password=data['password']) )
      else:  return json.dumps({"status":"fail1"})

  ## 로그인하기
  @app.route("/auth/login", methods=['POST'])
  @app.expect(model3)
  class Login(Resource):
    def post(self):
      if not referer(): return "",404
      data = postData()
      if 'email' in data.keys() and 'password' in data.keys():
        data2 = loginUser(email=data['email'])
        #print(json.dumps(data2))
        from util.password import check_password
        if check_password(password=data['password'], password2=data2['password']):
            from util.myjwt import makeToken
            import uuid
            tokenId = str(uuid.uuid4())
            accessToken = makeToken(tokenId=tokenId, tokenType='access', nickname=data2['nickname'],accountid=data2['accountid'] ).decode('utf-8')
            refreshToken = makeToken(tokenId=tokenId, tokenType='refresh', nickname=data2['nickname'],accountid=data2['accountid'] ).decode('utf-8')
      
            return json.dumps({"accessToken":accessToken, "refreshToken":refreshToken})
        else:  return json.dumps({"status":"fail2"})
      
      else:  return json.dumps({"status":"fail1"})

  ##  accessToken 다시 발급하기
  @app.route("/auth/refresh", methods=['POST'])
  @app.expect(model4)
  class Refresh(Resource):
    def post(self):
      if not referer(): return "",404
      data = postData()
      if 'token' in data.keys(): #and 'jti' in data.keys():
        from util.myjwt import refreshToken 
        return refreshToken(refresh=data['token']) #,tokenid=data['jti'])
      else:  return json.dumps({"status":"fail1"})

  ## token 확인 및 role 체크
  @app.route("/auth/checkrole", methods=['GET'])
  class Checkrole(Resource):
    @app.doc(security='apikey')
    def get(self):
      if not referer(): return "1",404
      data = headerAuth()
      if "access" in data['type']:
        return json.dumps({"role":data['role']})
      else: return "2",404

