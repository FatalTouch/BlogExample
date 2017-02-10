import hashlib
import random
import hmac

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
secret = '6v6_e8vs2@qh*!zy%dw(&_fx7aol^x$1z(6=a9_)z&+$y%(788'


def create_salt(length=6):
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(username, password, salt=None):
    if not salt:
        salt = create_salt()
    h = hashlib.sha384(username + password + salt).hexdigest()
    return '%s|%s' % (h, salt)


def create_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val,
                                    digestmod=hashlib.sha256).hexdigest())


def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == create_secure_val(val):
        return val


def basic_escape(text):
    return text.replace('<', '&lt;').replace('>', '&gt;')
