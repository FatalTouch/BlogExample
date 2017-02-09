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
    username = db.StringProperty(required=True)
    comment_count = db.IntegerProperty(default=0)

    @classmethod
    def create(cls, subject, content, username):
        blogpost = cls(subject=subject, content=content, username=username)
        blogpost.put()
        return blogpost

    @classmethod
    def get_latest(cls):
        return db.GqlQuery("Select * From BlogPost ORDER BY created desc limit 15")

    @classmethod
    def exists(cls, post_id):
        if post_id:
            if BlogPost.get_by_id(int(post_id)):
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def delete_post(cls, post_id):
        comments = Comments.get_comments_by_post(post_id)
        for c in comments:
            c.delete()
        cls.get_by_id(int(post_id)).delete()


class Comments(db.Model):
    comment = db.StringProperty(required=True)
    username = db.StringProperty(required=True)
    post_id = db.IntegerProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def create(cls, comment, username, post_id):
        comment = cls(comment=comment, username=username, post_id=int(post_id))
        comment.put()
        post = BlogPost.get_by_id(int(post_id))
        post.comment_count += 1
        post.put()
        return comment

    @classmethod
    def get_comments_by_post(cls, post_id):
        return cls.all().filter('post_id = ', int(post_id)).order('-created')

    @classmethod
    def delete_comment(cls, comment_id):
        comment = cls.get_by_id(int(comment_id))
        post = BlogPost.get_by_id(comment.post_id)
        post.comment_count -= 1
        post.put()
        comment.delete()



