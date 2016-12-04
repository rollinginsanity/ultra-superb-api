#Helpers specific to the auth endpoint, such as generate an oAuth token, and validate a refresh token.
import random

def tokenGenerator(length):
    #Defining some characters that will be used.
    chars = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-+=~"
    #Yay, we have a token, probably generated pretty badly. But that's the point!
    token = ''.join([chars[random.randint(0,len(chars))] for i in range(0,length)])

    return token
