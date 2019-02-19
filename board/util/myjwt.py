from config import secret, accesstokendurationSeconds, refreshtokendurationSeconds, audience
import jwt
from datetime import datetime, timedelta

## accessToken, refreshToken 체크
def checkToken(token):

    if not str(type(token)) in "<class 'bytes'>":
        token = bytes(token, 'utf-8')
    try:
        decoded = jwt.decode(token, secret, algorithm='HS256', audience=audience)
        #print(decoded)
          
        #print(decoded['jti'])
        return {"type":decoded['type'], "role":decoded["role"], 'jti':decoded["jti"], 'token':token, 'nickname':decoded['nickname'], 'accountid':decoded['accountid'] }
    except jwt.exceptions.ExpiredSignatureError:
        #print("expired")
        return {"type":"exprired"}
    except :
        #print("eroor")
        return {"type":"error1"}


## 접속을 위한 token의 발급
def makeToken(tokenId, tokenType, nickname, accountid):
    starttime = datetime.utcnow()
    endtime  = datetime.utcnow() + timedelta(seconds=accesstokendurationSeconds)
    if "refresh" in tokenType:
        endtime = datetime.utcnow() + timedelta(seconds=refreshtokendurationSeconds)
    
    #{"exp": 종료일시(unixtime), "nbf": 시작일시(unixtime), "aud": "ai.industrysolution.co.kr",  //수신자
    #"iat": 발급시간(unixtime), "jti": 발급식별ID}
    newToken = {"exp": endtime, "nbf": starttime, "aud": audience, "iat":starttime, "jti":tokenId, "type":tokenType, "role":10, "nickname":nickname, "accountid":accountid } 
    newTokenEncoded = jwt.encode(newToken, secret)

    return newTokenEncoded

## refreshToken을 통해 accessToken 재발급
def refreshToken(refresh):
    import json
    try:
        data = jwt.decode(refresh, secret)
        import uuid
        tokenId = str(uuid.uuid4())
        accessToken = makeToken(tokenId=tokenId, tokenType='access', nickname=data['nickname'] )

        return json.dumps({"accessToken":accessToken, "refreshToken":refresh})
    except: return json.dumps({"status":"fail"})
