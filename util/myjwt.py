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
        return {"type":decoded['type'], "role":decoded["role"], 'jti':decoded["jti"], 'token':token }
    except jwt.exceptions.ExpiredSignatureError:
        #print("expired")
        return {"type":"exprired"}
    except :
        #print("eroor")
        return {"type":"error1"}


## 접속을 위한 token의 발급
def makeToken(tokenId, tokenType, levelCode, nickname):
    starttime = datetime.utcnow()
    endtime  = datetime.utcnow() + timedelta(seconds=accesstokendurationSeconds)
    if "refresh" in tokenType:
        endtime = datetime.utcnow() + timedelta(seconds=refreshtokendurationSeconds)
    
    #{"exp": 종료일시(unixtime), "nbf": 시작일시(unixtime), "aud": "ai.industrysolution.co.kr",  //수신자
    #"iat": 발급시간(unixtime), "jti": 발급식별ID}
    newToken = {"exp": endtime, "nbf": starttime, "aud": audience, "iat":starttime, "jti":tokenId, "type":tokenType, "role":levelCode, "nickname":nickname } 
    newTokenEncoded = jwt.encode(newToken, secret)

    return newTokenEncoded
