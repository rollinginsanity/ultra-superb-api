#Helpers specific to the auth endpoint, such as generate an oAuth token, and validate a refresh token.
import random
import hashlib, binascii
from ultraSuperbAPI.models import auth_models

def tokenGenerator(length):
    #Defining some characters that will be used.
    chars = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-+=~" #Todo, change this to something really bad.
    #chars = "abcdABCD1234"  #Like this?
    #Yay, we have a token, probably generated pretty badly. But that's the point!
    token = ''.join([chars[random.randint(0,len(chars)-1)] for i in range(0,length)])

    return token

def validateCredentials(username, password, client_id):
    if validateClientID(client_id):
        return {"authenticated": True}
    else:
        return {"authenticated": False, "error": "missing or invalid client ID."} #Hint, this is bad, because it will help enumeration.


#Validate if a client ID is real.
def validateClientID(client_id):
    check_key = auth_models.APIKey.query.filter_by(key_value=client_id).first()

    if check_key:
        print("User authenticating with client_id: "+check_key.key_value)
        return True
    else:
        return False

def hashPassword(password_clear):
    password_hash_bytes = hashlib.pbkdf2_hmac('sha512', password_clear.encode(), b'This is a salt', 100000)

    #Convert output to a string.
    password_hash_hex = binascii.hexlify(password_hash_bytes)
    return password_hash_hex.decode('utf-8')
