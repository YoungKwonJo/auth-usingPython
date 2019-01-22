# python backend example code for authrization 


config.py 파일 만들기

```
secret = "secret"
accesstokendurationSeconds =  24*60*30 # 30 분
refreshtokendurationSeconds = 7*24*60*60 # 1 주일

smtpdomain = ''
smtpport = 587
smtpEmail = ''
smtpPwd = ''

hostname = ""
debug= True


host     = 'localhost'
user     = ''
password = ''
database = ''

dbaccess= ("%s:%s@%s/%s"%(user,password,host,database ))
audience="localhost"

```