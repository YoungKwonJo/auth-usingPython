from config import smtpdomain, smtpport, smtpEmail, smtpPwd, hostname

## 이메일의 글자들을 보고 유효성 검증
def validateEmailPattern(email):
    if len(email) > 5:
        import re
        #match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,7})$', email)
        match = re.match('^(([^<>()\[\]\.,;:\s@"]+(\.[^<>()\[\]\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$', email)

        if match != None:
            return True
    return False

## 진짜 사용하는 이메일 인지 확인하는 메일 보내기
def sendEmail(nickname, email, title, content):
    if not validateEmailPattern(email):
        return False
    try:
        import smtplib
        from email.mime.text import MIMEText
         
        smtp = smtplib.SMTP(smtpdomain, smtpport)
        smtp.ehlo()      # say Hello
        smtp.starttls()  # TLS 사용시 필요
        smtp.login(smtpEmail, smtpPwd)
        
        msg = MIMEText(content,'html') 
        msg['Subject'] = title
        msg['To'] = nickname #email 
        #print("send email...")
        
        smtp.sendmail(smtpEmail, email, msg.as_string())
         
        smtp.quit()
        return True
    except: return False

def sendEmail2( email, title, content):
    if not validateEmailPattern(email):
        return False

    import smtplib
    from email.mime.text import MIMEText
    try: 
        smtp = smtplib.SMTP(smtpdomain, smtpport)
        smtp.ehlo()      # say Hello
        smtp.starttls()  # TLS 사용시 필요
        smtp.login(smtpEmail, smtpPwd)
        
        msg = MIMEText(content,'html') 
        msg['Subject'] = title
        msg['To'] = email 
        #print("send email2...")
        
        smtp.sendmail(smtpEmail, email, msg.as_string())
         
        smtp.quit()
        
        return True
    except: return False
