import hashlib
import random
import hmac
import logging
# Letters that are used to create a salt
letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
# Secret key that is used to make a secure value
secret = '6v6_e8vs2@qh*!zy%dw(&_fx7aol^x$1z(6=a9_)z&+$y%(788'


# function to create a salt with a default length of 6
def create_salt(length=6):
    return ''.join(random.choice(letters) for x in xrange(length))


# function to create a hash by passing username and password
# salt can be passed in to make comparisons
def make_pw_hash(username, password, salt=None):
    if not salt:
        salt = create_salt()
    h = hashlib.sha384(username + password + salt).hexdigest()
    return '%s|%s' % (h, salt)


# function to create a secure value by using the hmac with our
# "secret" key
def create_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val,
                                    digestmod=hashlib.sha256).hexdigest())


# function to check if an existing secure value created by us
# is not tampered with
def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == create_secure_val(val):
        return val


# A basic escape function to escape html tags in user input
def basic_escape(text):
    return text.replace('<', '&lt;').replace('>', '&gt;')


def is_valid_int64(i):
    try:
        i = int(i)
        if i.bit_length() > 63:
            return False
        else:
            return True
    except ValueError:
        return False


def log(msg):
    logging.info(msg)

