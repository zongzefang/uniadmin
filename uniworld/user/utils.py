from itsdangerous import URLSafeTimedSerializer as utsr
from django.core.mail import send_mail, EmailMessage
from django.core.files import File
from uniworld.settings import SECRET_KEY,DOMAIN, DEFAULT_FROM_EMAIL
from user.models import UniUser
from other.models import University
import json
import csv
import base64
import re

class Token():
    def __init__(self,security_key):
        self.security_key = security_key
        self.salt = base64.encodebytes(bytes(security_key.encode('utf-8')))
    def generate_validate_token(self,username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username,self.salt)
    def confirm_validate_token(self,token,expiration=86400):
        serializer = utsr(self.security_key)
        return serializer.loads(token,
                salt=self.salt,
                max_age=expiration)

def EmailVerification(username, email):
    suffix=email.split('@')[1]
    for university in University.objects.all():
        if suffix.find(university.email_suffix)!=-1:
            Tok=Token(SECRET_KEY)
            token = Tok.generate_validate_token(username)
            message = '\n'.join([
                'Welcome to Univord, {0}!'.format(username),
                'Please click the following link to complete your registration',
                '/'.join([DOMAIN,'activate',token+'/'])
            ])
            mail=EmailMessage(
                'Univord email verification',
                message,
                DEFAULT_FROM_EMAIL,
                [email])
            mail.send()
            return university
    return False

def Confirm(token):
    Tok=Token(SECRET_KEY)
    return Tok.confirm_validate_token(token)
