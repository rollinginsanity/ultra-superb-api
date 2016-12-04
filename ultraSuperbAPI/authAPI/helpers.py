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
        auth_attempt = validatePassword(username, password)
        print(auth_attempt)
        if auth_attempt["valid"]:
            return {"authenticated": True, "user_id": auth_attempt["user_id"]}
        else:
            return {"authenticated": False, "error": auth_attempt["reason"]} #See below why this is baaaaad.
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

#Validate the user's password (and implicitly, the user at the same time.)
def validatePassword(username, password_clear):
    user = auth_models.User.query.filter_by(username=username).first()
    if user:
        if user.password == hashPassword(password_clear):     #Bad, should hash before getting user info, only hasing on valid values leads to enumeration.
            return {"valid": True, "user_id": user.id}
        else:
            return {"valid": False, "reason": "Incorrect password for user."} #Nononononono, never do this.
    else:
        return {"valid": False, "reason": "User does not exist."} #Also bad.

def hashPassword(password_clear):
    password_hash_bytes = hashlib.pbkdf2_hmac('sha512', password_clear.encode(), b'This is a salt', 100000)

    #Convert output to a string.
    password_hash_hex = binascii.hexlify(password_hash_bytes)
    return password_hash_hex.decode('utf-8')

def validateAccessToken(access_token):
    token = access_token.split(" ")[1]
    token_check = auth_models.oAuthAccessToken.query.filter_by(token_value=token).first()
    if token_check:
        return {"valid": True, "user_id": token_check.user_id}
    else:
        return {"valid": False}