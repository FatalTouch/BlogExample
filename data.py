from google.appengine.ext import db
import helpers
import validate


# User entity
class User(db.Model):
    # Information to store in the user entity
    username = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)

    # Class method that can be called to create a user
    @classmethod
    def create_user(cls, username, password, email=None):

        # Hash the pw before saving in database
        hashed_pw = helpers.make_pw_hash(username, password)

        # Save the username in lower case in database
        username = username.lower()

        # Check if email exists and convert it to lower case and save in db
        if email:
            email = email.lower()
            user = cls(username=username, pw_hash=hashed_pw, email=email)
        else:
            user = cls(username=username, pw_hash=hashed_pw)

        # Write the entity to database
        user.put()

        # Return the user that was created
        return user

    # Method to check if the username exists in the database
    @classmethod
    def check_username(cls, username):
        return cls.all().filter('username = ', username.lower()).get()

    # Method to authenticate the user by comparing the password and hashed
    # password
    @classmethod
    def authenticate(cls, username, password):
        username = username.lower()
        user = User.all().filter('username = ', username).get()
        if (user and validate.is_valid_password_hash
            (username, password, user.pw_hash)):
            return user


# Blog post entity
class BlogPost(db.Model):
    # Information to store in the blog post entity
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    username = db.StringProperty(required=True)
    comment_count = db.IntegerProperty(default=0)

    # Method to create a blog post
    @classmethod
    def create(cls, subject, content, username):
        blogpost = cls(subject=subject, content=content, username=username)
        blogpost.put()
        return blogpost

    # Method to edit a blog post
    @classmethod
    def edit(cls, subject, content, post_id):
        blogpost = cls.get_by_id(int(post_id))
        if blogpost:
            blogpost.content = content
            blogpost.subject = subject
            blogpost.put()
            return True

    # Method to get 15 latest blog posts
    @classmethod
    def get_latest(cls):
        return db.GqlQuery("Select * From BlogPost "
                           "ORDER BY created desc limit 15")

    # Method to check if a blog post exists
    @classmethod
    def exists(cls, post_id):
        if post_id:
            if BlogPost.get_by_id(int(post_id)):
                return True
            else:
                return False
        else:
            return False

    # Method to delete a blog post and it's associated data
    @classmethod
    def delete_post(cls, post_id):
        comments = Comments.get_comments_by_post(post_id)
        for c in comments:
            c.delete()
        likes = Likes.get_likes_by_post(post_id)
        for l in likes:
            l.delete()
        cls.get_by_id(int(post_id)).delete()


# Comments entity
class Comments(db.Model):
    # Information stored in the comments entity
    comment = db.StringProperty(required=True)
    username = db.StringProperty(required=True)
    post_id = db.IntegerProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

    # Method to create a new comment
    @classmethod
    def create(cls, comment, username, post_id):
        comment = comment.replace('\n', ' ')
        comment = cls(comment=comment, username=username, post_id=int(post_id))
        comment.put()
        post = BlogPost.get_by_id(int(post_id))
        post.comment_count += 1
        post.put()
        return comment

    # Method to edit an existing comment
    @classmethod
    def edit(cls, comment, comment_id, username):
        comment = comment.replace('\n', ' ')
        db_comment = cls.get_by_id(int(comment_id))
        if db_comment.key().id() == int(comment_id):
            if not db_comment.username == username:
                return None
            db_comment.comment = comment
            db_comment.put()
            return True

    # Method to get all the comments by passing a post id ordered by
    # time they were created in descending order
    @classmethod
    def get_comments_by_post(cls, post_id):
        return cls.all().filter('post_id = ', int(post_id)).order('-created')

    # Method to delete a comment
    @classmethod
    def delete_comment(cls, comment_id):
        comment = cls.get_by_id(int(comment_id))
        post = BlogPost.get_by_id(comment.post_id)
        post.comment_count -= 1
        post.put()
        comment.delete()


# Likes entity
class Likes(db.Model):
    # Information stored in the likes entity
    username = db.StringProperty(required=True)
    post_id = db.IntegerProperty(required=True)
    value = db.BooleanProperty(required=True)

    # Method to create a new like and do a check before to make sure that
    # the person liking/unliking the post isn't the creator of the post
    @classmethod
    def create(cls, username, post_id, value):
        post = BlogPost.get_by_id(int(post_id))
        if post:
            if not post.username == username:
                db_likes = (cls.all().filter('post_id = ', int(post_id))
                            .filter('username = ', username)).get()
                if db_likes:
                    db_likes.value = value
                    db_likes.put()
                    return True
                else:
                    db_likes = cls(username=username, post_id=int(post_id),
                                   value=value)
                    db_likes.put()
                    return True

    # like method that calls the create method with a True value for like
    @classmethod
    def like(cls, username, post_id):
        return cls.create(username, post_id, True)

    # dislike method that calls the create method with a False value for like
    @classmethod
    def unlike(cls, username, post_id):
        return cls.create(username, post_id, False)

    # Get the current like status for a post by passing in username and postid
    @classmethod
    def get_status(cls, username, post_id):
        status = (cls.all().filter('post_id = ', int(post_id))
                  .filter('username = ', username)).get()

        if status:
            return status.value
        else:
            return False

    # Get all the likes by passing in a post_id
    @classmethod
    def get_likes_by_post(cls, post_id):
        return cls.all().filter('post_id = ', int(post_id))

    # Get the total likes for a post
    @classmethod
    def get_total_likes(cls, post_id):
        return (cls.all().filter('post_id = ', int(post_id))
                .filter('value = ', True)).count()
