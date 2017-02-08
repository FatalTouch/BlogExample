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


class BlogPost(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    user_id = db.IntegerProperty(required=True)

    @classmethod
    def create(cls, subject, content, user_id):
        blogpost = cls(subject=subject, content=content, user_id=user_id)
        blogpost.put()
        return blogpost

    @classmethod
    def get_latest(cls):
        return db.GqlQuery("Select * From BlogPost ORDER BY created desc limit 15")


