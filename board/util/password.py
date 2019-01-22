
# https://docs.python.org/3/library/hashlib.html
def hash_password(password):
  import hashlib, binascii
  import os
  salt =os.urandom(16)
  salt = binascii.hexlify(salt)
  dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
  
  print(salt)
  print(binascii.hexlify(dk))
  print(len(binascii.hexlify(dk)))

  return (binascii.hexlify(dk)+salt).decode('utf-8')

def check_password(password, password2):
  if not str(type(password2)) in "<class 'bytes'>":
      password2 = password2.encode('utf-8')
  import hashlib, binascii
  salt = password2[64:]
  dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

  print(salt)
  print(binascii.hexlify(dk))
  print(len(binascii.hexlify(dk)))

  return password2 == binascii.hexlify(dk)+salt