from google.appengine.ext import db
import helpers


class User(db.Model):
    username = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)


def create_user(username, password, email=None):
    hashed_pw = helpers.make_pw_hash(username, password)
    username = username.lower()
    if email:
        email = email.lower()
        user = User(username=username, pw_hash=hashed_pw, email=email)
    else:
        user = User(username=username, pw_hash=hashed_pw)
    user.put()
    return user


def check_username(username):
    return User.all().filter('username = ', username.lower()).get()


def authenticate(username, password):
    username = username.lower()
    user = User.all().filter('username = ', username).get()
    if user and helpers.is_valid_password_hash(username, password, user.pw_hash):
        return user


def get_user_by_id(uid):
    return User.get_by_id(uid)

