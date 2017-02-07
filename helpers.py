import re
import hashlib
import hmac
import random
import bcrypt


# User Registration input validations
def is_valid_username(username):
    if username:
        user_re = re.compile(r"^[a-zA-Z0-9_-]{4,20}$")
        if user_re.match(username):
            return None
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


def make_salt(length = 6):
    return ' '.join(random.choice(letters) for x in xrange(length))

