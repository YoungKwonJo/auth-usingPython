import json
from flask import render_template, request

import uuid
from datetime import datetime, timedelta

from route.base import postData, errror, headerAuth, referer, doIt
from action.auth import checkEmail, insertUser, loginUser

def auth(app):
  @app.route("/auth/")
  def test1():
    return "test route"

 
  @app.route("/auth/error", methods=['POST'])
  def error1():
     #import json
     return json.dumps({"error":"error"}),404

   ## 가입여부 확인 
  @app.route("/auth/checkemail", methods=['POST'])
  def checkemail():
    data = postData()
    if 'email' in data.keys():
      return doIt(checkEmail(email=data['email']))
    else:  return json.dumps({"status":"fail1"})
 

  ## 가입하기 
  @app.route("/auth/signin", methods=['POST'])
  def signin():
    data = postData()
    if 'nickname' in data.keys() and 'password' in data.keys():
      from util.password import hash_password
      password= hash_password(data['password'])
      return doIt(insertUser(nickname=data['nickname'],email=data['email'], password=password) )
      #return doIt(insertUser(nickname=data['nickname'],email=data['email'], password=data['password']) )
    else:  return json.dumps({"status":"fail1"})

  ## 로그인하기
  @app.route("/auth/login", methods=['POST'])
  def login():
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
  def refresh():
    if not referer(): return "",404
    data = postData()
    if 'refresh' in data.keys() :
      from util.myjwt import refreshToken 
      return refreshToken(token=data['token'],tokenid=data['jti'])
    else:  return json.dumps({"status":"fail1"})

  ## token 확인 및 role 체크
  @app.route("/auth/checkrole", methods=['GET'])
  def checkrole():
    if not reffer(): return "1",404
    data = headerAuth()
    if "access" in data['type']:
      return json.dumps({"role":data['role']})
    else: return "2",404


