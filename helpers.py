import re
import hashlib
import random
import data
import hmac


# User Registration input validations
def is_valid_username(username):
    if username:
        user_re = re.compile(r"^[a-zA-Z0-9_-]{4,20}$")
        if user_re.match(username):
            if not data.check_username(username):
                return None
            else:
                return "Username already exists"
        else:
            return ("User name is not valid. Please make sure "
                    "it is between 4-20 characters and doesn't "
                    "contain any special symbols.")
    else:
        return "*Username can't be empty."


def is_valid_password(password, verify):
    if password and verify:
        if password != verify:
            return "Password and confirmation password do not match"
        else:
            password_re = re.compile(r"^.{6,30}$")
            if password_re.match(password):
                return None
            else:
                return ("Password is not valid. Please make sure it is "
                        "between 6-30 characters.")
    else:
        return "Password or confirmation password can't be empty."


def is_valid_email(email):
    if email:
        email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        if email_re.match(email):
            return None
        else:
            return "Email address entered is not valid."
    else:
        return None


letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def create_salt(length=6):
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(username, password, salt=None):
    if not salt:
        salt = create_salt()
    h = hashlib.sha384(username + password + salt).hexdigest()
    return '%s|%s' % (h, salt)


def is_valid_password_hash(username, password, h):
    salt = h.split('|')[1]
    return h == make_pw_hash(username, password, salt)


secret = '6v6_e8vs2@qh*!zy%dw(&_fx7aol^x$1z(6=a9_)z&+$y%(788'


def create_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val, digestmod=hashlib.sha256).hexdigest())


def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == create_secure_val(val):
        return val

