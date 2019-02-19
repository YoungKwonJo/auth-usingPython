import json
from flask import render_template, request

from config import hostname, debug
from util.myjwt import checkToken

def postData():
    data = {}
    if 'x-www-form-urlencoded' in request.headers.get('Content-Type'):
       for i in  request.form.keys():
           data[i] = request.form[i]
    elif 'json' in request.headers.get('Content-Type'):
       data = request.get_json()
    else :
       data = request.get_data()
       data['error']='use header for content-type: application/x-www-form-urlencoded or application/json'
    return data
def errror():
    return json.dumps({"error":"error"})

def headerAuth():
    auth_header = request.headers['Authorization2']
    #print(auth_header)
    #auth_header = request.headers.get('Authorization2')
    try:
        auth_token = auth_header.split(" ")[1]
        return checkToken(auth_token)
    except: 
        return {"type":"error0"}
    #print("auth_token")
    #print(auth_token)
    #if 'NoneType' in str(type(auth_token)):
    #    return {"type":"error0"}
    #else:  return checkToken(auth_token) 

def referer():
    referer = request.headers.get('referer')
    #print(referer)
    if 'NoneType' in str(type(referer)):  return debug
    if not hostname in referer: return debug
    #print(referer) 
    return True


def doIt(function):
    if function: 
        return json.dumps({"status":"success"})
    else:  return json.dumps({"status":"fail"})
